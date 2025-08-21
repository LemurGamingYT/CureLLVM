from logging import debug, info, warning
from typing import cast

from llvmlite import ir as lir, binding as llvm

from cure.c_registry import CRegistry
from cure.passes import CompilerPass
from cure import ir
from cure.codegen_utils import (
    NULL, create_while_loop, store_in_pointer, create_string_constant, get_struct_ptr_field,
    get_struct_value_field, index_of_type, create_ternary
)


DONT_MANAGE_MEMORY = (
    ir.Type, ir.Param, ir.Function, ir.Variable, ir.Id, ir.Body, ir.Assignment, ir.Elif,
    ir.If, ir.While, ir.Return
)


class CodeGeneration(CompilerPass):
    def __init__(self, scope):
        super().__init__(scope)

        info('Initialising LLVM')

        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.module = lir.Module('main')
        self.module.triple = llvm.get_default_triple()

        self.builder = lir.IRBuilder()

        info('Created module and builder')
        debug(f'Target = {self.module.triple}')

        self.c_registry = CRegistry(self.module, scope)

        registered_functions_str = ', '.join(self.c_registry.get_registered_functions())
        debug(f'Registered: {registered_functions_str}')

        self.return_value = None

        setattr(self.module, 'c_registry', self.c_registry)
    
    def _decrement_reference(self, pos: ir.Position, struct, type: ir.Type):
        Ref = cast(ir.Type, self.scope.type_map.get('Ref'))
        ref_index = index_of_type(type.type, lir.PointerType(Ref.type))
        if ref_index == -1:
            warning(f'Type {type} needs memory management but has no Ref* field')
            return

        ref = self.builder.load(get_struct_ptr_field(self.builder, struct, ref_index)) if\
            isinstance(struct.type, lir.PointerType) else\
            get_struct_value_field(self.builder, struct, ref_index)
        
        self.scope.call(pos, self.builder, self.module, 'Ref.dec', [
            ir.CallArgument(ref, Ref.as_pointer())
        ])
    
    def _increment_reference(self, pos: ir.Position, struct, type: ir.Type):
        Ref = cast(ir.Type, self.scope.type_map.get('Ref'))
        ref_index = index_of_type(type.type, lir.PointerType(Ref.type))
        if ref_index == -1:
            warning(f'Type {type} needs memory management but has no Ref* field')
        else:
            ref = get_struct_value_field(self.builder, struct, ref_index)
            self.scope.call(pos, self.builder, self.module, 'Ref.inc', [
                ir.CallArgument(ref, Ref.as_pointer())
            ])
    
    def run_on(self, node: ir.Node):
        node_type = node.type
        if isinstance(node, DONT_MANAGE_MEMORY) or not node_type.needs_memory_management(self.scope):
            return super().run_on(node)
        
        value = super().run_on(node)
        if isinstance(value.type, lir.PointerType):
            value = self.builder.load(value)
        
        if isinstance(value.type, (lir.LiteralStructType, lir.IdentifiedStructType)):
            self._increment_reference(node.pos, value, node_type)

        ptr = store_in_pointer(self.builder, node_type.type, value, 'temp_var')
        self.scope.symbol_table.add(ir.Symbol(ptr.name, node_type, ptr))
        return self.builder.load(ptr, 'temp')
    
    def run_on_Type(self, node: ir.Type):
        return node.type
    
    def run_on_Program(self, node: ir.Program):
        info('Compiling program')
        for n in node.nodes:
            self.run_on(n)
        
        return str(self.module)
    
    def cleanup(self, pos: ir.Position):
        info('Cleaning up')

        memory_management_symbols = [
            symbol for symbol in self.scope.symbol_table.local_symbols.values()
            if symbol.type.needs_memory_management(self.scope)
        ]

        if len(memory_management_symbols) == 0:
            info('No memory management symbols found')
            return
        
        cleanup_block = self.builder.function.append_basic_block('cleanup')
        old_builder = self.builder
        self.builder.branch(cleanup_block)
        self.builder.position_at_end(cleanup_block)
        for symbol in memory_management_symbols:
            symbol_type = symbol.type
            self._decrement_reference(pos, symbol.value, symbol_type)
        
        self.builder.position_at_end(old_builder.block)
        info('Finished cleanup')
    
    def run_on_Body(self, node: ir.Body):
        self.scope = self.scope.clone()
        info('Compiling body')

        has_cleaned_up = False
        for stmt in node.nodes:
            info(f'Compiling body statement {stmt.__class__.__name__}')
            if isinstance(stmt, ir.Return):
                self.cleanup(stmt.pos)
                has_cleaned_up = True
            
            self.run_on(stmt)
            info(f'Compiled body statement {stmt.__class__.__name__}')
        
        if not has_cleaned_up:
            self.cleanup(node.pos)
        
        info('Compiled body')
        self.scope = cast(ir.Scope, self.scope.parent)
    
    def run_on_If(self, node: ir.If):
        func = self.builder.function
        merge_block = func.append_basic_block('if_merge')
        then_block = func.append_basic_block('if_then')

        elif_test_blocks = []
        elif_then_blocks = []

        for i, _ in enumerate(node.elseifs):
            elif_test_blocks.append(func.append_basic_block(f'elif_test_{i}'))
            elif_then_blocks.append(func.append_basic_block(f'elif_then_{i}'))

        else_block = func.append_basic_block('if_else') if node.else_body else merge_block

        # Evaluate main condition
        cond = self.run_on(node.condition)
        first_elif_test = elif_test_blocks[0] if elif_test_blocks else else_block
        self.builder.cbranch(cond, then_block, first_elif_test)

        # THEN block
        self.builder.position_at_end(then_block)
        then_value = self.run_on(node.body)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)
        then_end_block = self.builder.block

        # ELIF chain
        elif_end_blocks = []
        elif_values = []

        for i, elif_node in enumerate(node.elseifs):
            # Test block
            self.builder.position_at_end(elif_test_blocks[i])
            elif_cond = self.run_on(elif_node.condition)

            next_target = elif_test_blocks[i + 1] if i + 1 < len(elif_test_blocks) else else_block
            self.builder.cbranch(elif_cond, elif_then_blocks[i], next_target)

            # Then block for this elif
            self.builder.position_at_end(elif_then_blocks[i])
            elif_value = self.run_on(elif_node.body)
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)
            elif_end_blocks.append(self.builder.block)
            elif_values.append(elif_value)

        # ELSE block
        if else_block is not merge_block:
            self.builder.position_at_end(else_block)
            else_value = self.run_on(cast(ir.Body, node.else_body))
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)
            else_end_block = self.builder.block
        else:
            else_value = None
            else_end_block = None

        # Merge
        self.builder.position_at_end(merge_block)

        # If we got values from all branches, build PHI
        all_values = [then_value] + elif_values + ([else_value] if else_value is not None else [])
        all_blocks = [then_end_block] + elif_end_blocks + ([else_end_block] if else_end_block else [])

        if all(v is not None for v in all_values):
            phi = self.builder.phi(all_values[0].type)
            for val, blk in zip(all_values, all_blocks):
                phi.add_incoming(val, blk)
            return phi

        return None

    def run_on_While(self, node: ir.While):
        def cond(builder):
            old_builder = self.builder
            self.builder = builder

            res = self.run_on(node.condition)

            self.builder = old_builder
            return res

        def body(builder):
            old_builder = self.builder
            self.builder = builder
            
            self.run_on(node.body)

            self.builder = old_builder

        create_while_loop(self.builder, cond, body)
    
    def run_on_Param(self, node: ir.Param):
        return self.run_on(node.type)
    
    def run_on_Function(self, node: ir.Function):
        info(f'Compiling function {node.name}')
        ret_type = self.run_on(node.type)
        param_types = [self.run_on(param) for param in node.params]
        func = lir.Function(self.module, lir.FunctionType(ret_type, param_types), node.name)
        setattr(func, 'params', node.params)

        self.scope.symbol_table.add(ir.Symbol(
            node.name, cast(ir.Type, self.scope.type_map.get('function')), func
        ))
        
        if isinstance(node.body, ir.Body):
            info('Compiling function body')

            old_builder = self.builder
            entry_block = func.append_basic_block('entry')
            self.builder = lir.IRBuilder(entry_block)
            if len(node.params) > 0:
                param_allocation_block = func.append_basic_block('param_allocation')
                self.builder.position_at_end(param_allocation_block)

                for i, param in enumerate(node.params):
                    param_value = func.args[i]
                    type = param.type
                    if type.needs_memory_management(self.scope):
                        self._increment_reference(node.pos, param_value, type)
                    
                    if param.is_mutable:
                        param_value = store_in_pointer(
                            self.builder, type.type, param_value, f'{param.name}_ptr'
                        )
                    
                    self.scope.symbol_table.add(ir.Symbol(
                        param.name, type, param_value, param.is_mutable
                    ))
                
                self.builder.branch(entry_block)
                self.builder.position_at_end(entry_block)
            
            self.run_on(node.body)

            if node.type == self.scope.type_map.get('nil'):
                info(f'{node.name} has no return type, inserting ret NULL')
                self.return_value = NULL()
            
            if self.return_value is None:
                self.builder.ret_void()
            else:
                return_block = self.builder.function.append_basic_block('return')
                self.builder.branch(return_block)
                self.builder.position_at_end(return_block)

                self.builder.ret(self.return_value)
                self.return_value = None

            for param in node.params:
                self.scope.symbol_table.remove(param.name)

            self.builder = old_builder

        info(f'Finished compiling function {node.name}')
        return func
    
    def run_on_Variable(self, node: ir.Variable):
        value = self.run_on(node.value) if node.value is not None else node.value
        if value is None:
            node.pos.comptime_error('cannot generate code for uninitialised variables', self.scope.src)
            return

        symbol_value = value

        # if the variable is mutable, a pointer is allocated, if not, the variable's value replaces
        # it's use because it will never change, it's basically a constant
        if node.is_mutable:
            symbol_value = store_in_pointer(
                self.builder, self.run_on(node.type), symbol_value, node.name
            )
        
        self.scope.symbol_table.add(ir.Symbol(node.name, node.type, symbol_value, node.is_mutable))
        return symbol_value
    
    def run_on_Assignment(self, node: ir.Assignment):
        value = self.run_on(node.value)
        symbol = cast(ir.Symbol, self.scope.symbol_table.get(node.name))
        if not symbol.is_mutable:
            node.pos.comptime_error(f'\'{node.name}\' is immutable', self.scope.src)

        ptr = symbol.value
        return self.builder.store(value, ptr)
    
    def run_on_Return(self, node: ir.Return):
        # if self.return_value is not None:
        #     node.pos.comptime_error('cannot return twice', self.scope.src)
        
        value = self.run_on(node.value)
        self.return_value = value
        info(f'Returning {value}')
        return value
    
    def run_on_Int(self, node: ir.Int):
        return lir.Constant(self.run_on(node.type), node.value)
    
    def run_on_Float(self, node: ir.Float):
        return lir.Constant(self.run_on(node.type), node.value)
    
    def run_on_String(self, _):
        raise NotImplementedError
    
    def run_on_Bool(self, node: ir.Bool):
        return lir.Constant(self.run_on(node.type), node.value)
    
    def run_on_Nil(self, _):
        return NULL()
    
    def run_on_StringLiteral(self, node: ir.StringLiteral):
        s = node.value.encode('utf-8').decode('unicode_escape')
        return create_string_constant(self.module, s)
    
    def run_on_Id(self, node: ir.Id):
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            return
        
        if hasattr(symbol.value, 'type') and isinstance(symbol.value.type, lir.PointerType):
            info(f'Loading pointer {node.name}')
            return self.builder.load(symbol.value, node.name)
        
        info(f'Loading value {node.name}')
        return symbol.value
    
    def run_on_Call(self, node: ir.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        if symbol is None:
            node.pos.comptime_error(f'unknown symbol {node.callee}', self.scope.src)
            return
        
        args = [self.run_on(arg) for arg in node.args]
        if isinstance(symbol.value, ir.Function):
            return symbol.value(node.pos, self.scope, [
                ir.CallArgument(arg, arg_type) for arg, arg_type in zip(args, [
                    arg.type for arg in node.args
                ])
            ], self.module, self.builder)
        elif isinstance(symbol.value, lir.Function):
            ir_func = symbol.value
            return self.builder.call(ir_func, args, node.callee)
        else:
            node.pos.comptime_error(f'invalid callable {node.callee}', self.scope.src)
    
    def run_on_BinaryOp(self, _):
        raise NotImplementedError
    
    def run_on_UnaryOp(self, _):
        raise NotImplementedError
    
    def run_on_Attribute(self, _):
        raise NotImplementedError
    
    def run_on_Cast(self, _):
        raise NotImplementedError
    
    def run_on_Ternary(self, node: ir.Ternary):
        return create_ternary(
            self.builder, self.run_on(node.condition),
            self.run_on(node.true), self.run_on(node.false)
        )
