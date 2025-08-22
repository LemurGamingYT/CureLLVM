from logging import info
from typing import cast

from cure.codegen_utils import max_value, min_value
from cure.passes import CompilerPass
from cure import ir


INT_MAX = max_value(32)
INT_MIN = min_value(32)


class Analyser(CompilerPass):
    def run_on_Program(self, node: ir.Program):
        nodes = []
        for n in node.nodes:
            info(f'Analysing {n.__class__.__name__}')
            nodes.append(self.run_on(n))
        
        return ir.Program(node.pos, node.type, nodes)
    
    def run_on_Type(self, node: ir.Type):
        return node
    
    def run_on_PointerType(self, node: ir.PointerType):
        return self.run_on_Type(node.pointee)
    
    def run_on_ReferenceType(self, node: ir.ReferenceType):
        return self.run_on_Type(node.target)
    
    def run_on_Param(self, node: ir.Param):
        return ir.Param(node.pos, self.run_on(node.type), node.name, node.is_mutable)
    
    def run_on_Body(self, node: ir.Body):
        self.scope = self.scope.clone()

        info('Entered child scope for body')
        nodes = []
        for n in node.nodes:
            info(f'Analysing body node {n.__class__.__name__}')
            nodes.append(self.run_on(n))

        info('Exiting body')
        self.scope = cast(ir.Scope, self.scope.parent)
        return ir.Body(node.pos, node.type, nodes)
    
    def run_on_Elif(self, node: ir.Elif):
        return ir.Elif(
            node.pos, node.type,
            self.run_on(node.condition), self.run_on(node.body)
        )
    
    def run_on_If(self, node: ir.If):
        condition = self.run_on(node.condition)
        if condition.type != self.scope.type_map.get('bool'):
            node.pos.comptime_error('condition is not a boolean', self.scope.src)

        return ir.If(
            node.pos, node.type, condition, self.run_on(node.body),
            self.run_on(node.else_body) if node.else_body is not None else node.else_body,
            [self.run_on(elseif) for elseif in node.elseifs]
        )
    
    def run_on_While(self, node: ir.While):
        condition = self.run_on(node.condition)
        if condition.type != self.scope.type_map.get('bool'):
            node.pos.comptime_error('condition is not a boolean', self.scope.src)
        
        return ir.While(node.pos, node.type, condition, self.run_on(node.body))
    
    def run_on_Function(self, node: ir.Function):
        params = [self.run_on(param) for param in node.params]
        type = self.run_on(node.type)
        func = ir.Function(node.pos, type, node.name, params, node.body, node.flags, node.overloads)
        self.scope.symbol_table.add(ir.Symbol(
            node.name, cast(ir.Type, self.scope.type_map.get('function')), func
        ))

        info('Adding parameters to environment')
        for param in params:
            self.scope.symbol_table.add(ir.Symbol(param.name, param.type, param, param.is_mutable))
        
        body = self.run_on(node.body) if isinstance(node.body, ir.Body) else node.body

        info('Removing parameters from environment')
        for param in params:
            self.scope.symbol_table.remove(param.name)

        func.body = body
        return func
    
    def run_on_Variable(self, node: ir.Variable):
        value = self.run_on(node.value) if node.value is not None else node.value
        if (symbol := self.scope.symbol_table.get(node.name)) is not None and value is not None:
            if not symbol.is_mutable:
                node.pos.comptime_error(f'\'{node.name}\' is immutable', self.scope.src)

            return self.run_on(ir.Assignment(node.pos, value.type, node.name, value))
        
        var_type = value.type if value is not None else node.type
        self.scope.symbol_table.add(ir.Symbol(node.name, var_type, value, node.is_mutable))
        return ir.Variable(node.pos, var_type, node.name, value, node.is_mutable)
    
    def run_on_Assignment(self, node: ir.Assignment):
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            raise RuntimeError()

        symbol.value = node.value
        return node
    
    def run_on_Return(self, node: ir.Return):
        value = self.run_on(node.value)
        return ir.Return(node.pos, value.type, value)
    
    def run_on_Int(self, node: ir.Int):
        if node.value > INT_MAX:
            node.pos.comptime_error('integer value is too large for a 32-bit integer', self.scope.src)
        
        if node.value < INT_MIN:
            node.pos.comptime_error('integer value is too small for a 32-bit integer', self.scope.src)
        
        return node
    
    def run_on_Float(self, node: ir.Float):
        return node
    
    def run_on_String(self, node: ir.String):
        return self.run_on(ir.Call(node.pos, node.type, 'string.new', [
            ir.StringLiteral(node.pos, cast(ir.Type, self.scope.type_map.get('pointer')), node.value),
            ir.Int(node.pos, cast(ir.Type, self.scope.type_map.get('int')), len(node.value))
        ]))
    
    def run_on_Bool(self, node: ir.Bool):
        return node
    
    def run_on_Nil(self, node: ir.Nil):
        return node
    
    def run_on_StringLiteral(self, node: ir.StringLiteral):
        return node
    
    def run_on_Id(self, node: ir.Id):
        symbol = self.scope.symbol_table.get(node.name)
        type = self.scope.type_map.get(node.name)
        if symbol is None and type is None:
            node.pos.comptime_error(f'unknown identifier \'{node.name}\'', self.scope.src)
            return
        
        if symbol is not None:
            return ir.Id(node.pos, symbol.type, symbol.name)
        
        return ir.Id(node.pos, cast(ir.Type, type), node.name)
    
    def run_on_Call(self, node: ir.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        if symbol is None:
            return node.pos.comptime_error(f'unknown callable \'{node.callee}\'', self.scope.src)
        
        args = [self.run_on(arg) for arg in node.args]
        return symbol.value(node.pos, self.scope, args)
    
    def run_on_BinaryOp(self, node: ir.BinaryOp):
        lhs = self.run_on(node.left)
        rhs = self.run_on(node.right)
        ltype = lhs.type
        rtype = rhs.type
        op_name = ir.op_map[node.op]
        callee = f'{ltype}.{op_name}_{rtype}'
        if not self.scope.symbol_table.has(callee):
            node.pos.comptime_error(
                f'unsupported operation \'{node.op}\' between types \'{ltype}\' and \'{rtype}\'',
                self.scope.src
            )
        
        return self.run_on(ir.Call(node.pos, node.type, callee, [lhs, rhs]))
    
    def run_on_UnaryOp(self, node: ir.UnaryOp):
        expr = self.run_on(node.expr)
        op_name = ir.op_map[node.op]
        callee = f'{expr.type}_{op_name}'
        if not self.scope.symbol_table.has(callee):
            node.pos.comptime_error(
                f'unsupported operation \'{node.op}\' on type \'{expr.type}\'',
                self.scope.src
            )
        
        return self.run_on(ir.Call(node.pos, node.type, callee, [expr]))
    
    def run_on_Attribute(self, node: ir.Attribute):
        obj = self.run_on(node.obj)
        args = [obj] + ([self.run_on(arg) for arg in node.args] if node.args is not None else [])
        callee = f'{obj.type}.{node.attr}'
        if not self.scope.symbol_table.has(callee):
            node.pos.comptime_error(
                f'unknown attribute \'{node.attr}\' on type \'{obj.type}\'',
                self.scope.src
            )
        
        symbol = cast(ir.Symbol, self.scope.symbol_table.get(callee))
        func = symbol.value
        if func.flags.static:
            args = args[1:]
        
        return self.run_on(ir.Call(node.pos, node.type, callee, args))
    
    def run_on_Cast(self, node: ir.Cast):
        obj = self.run_on(node.obj)
        to_type = self.run_on(node.type)
        callee = f'{obj.type}.to_{to_type}'
        if not self.scope.symbol_table.get(callee):
            node.pos.comptime_error(
                f'cannot cast type \'{obj.type}\' to type \'{to_type}\'',
                self.scope.src
            )
        
        return self.run_on(ir.Call(node.pos, node.type, callee, [obj]))

    def run_on_Ternary(self, node: ir.Ternary):
        true = self.run_on(node.true)
        false = self.run_on(node.false)
        if true.type != false.type:
            node.pos.comptime_error(
                f'true and false types do not match (\'{true.type}\' and \'{false.type}\')',
                self.scope.src
            )

        condition = self.run_on(node.condition)
        if condition.type != self.scope.type_map.get('bool'):
            node.pos.comptime_error('condition is not a boolean', self.scope.src)

        return ir.Ternary(node.pos, true.type, condition, true, false)
