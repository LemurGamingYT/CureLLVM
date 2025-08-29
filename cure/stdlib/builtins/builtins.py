from typing import override

from llvmlite import ir as lir

from cure.codegen_utils import get_struct_field_value, index_of_type
from .float import float as floatClass
from .bool import bool as boolClass
from .int import int as intClass
from .string import string
from .Ref import Ref
from cure import ir


class builtins(ir.Lib):
    @override
    def init(self):
        self.scope.c_registry.register_function('puts', lir.FunctionType(lir.VoidType(), [
            lir.PointerType(lir.IntType(8))
        ]))

        self.scope.c_registry.register_function('snprintf', lir.FunctionType(lir.VoidType(), [
            lir.PointerType(lir.IntType(8)),
            lir.IntType(64),
            lir.PointerType(lir.IntType(8))
        ]))

        self.scope.c_registry.register_function('malloc', lir.FunctionType(
            lir.PointerType(lir.IntType(8)), [lir.IntType(64)]
        ))

        self.scope.c_registry.register_function('free', lir.FunctionType(lir.VoidType(), [
            lir.PointerType(lir.IntType(8))
        ]))

        self.scope.c_registry.register_function('memcpy', lir.FunctionType(lir.VoidType(), [
            lir.PointerType(lir.IntType(8)),
            lir.PointerType(lir.IntType(8)),
            lir.IntType(64)
        ]))

        self.scope.c_registry.register_function('strlen', lir.FunctionType(lir.IntType(64), [
            lir.PointerType(lir.IntType(8))
        ]))

        self.scope.c_registry.register_function('exit', lir.FunctionType(lir.VoidType(), [
            lir.IntType(32)
        ]))

        self.add(Ref)
        self.add(string)

        self.add(intClass)
        self.add(boolClass)
        self.add(floatClass)

        @ir.builtin(self, params=[
            ir.Param(ir.Position.zero(), ir.GenericType.from_name('T'), 'value')
        ], generic_params=['T'], override_name='print')
        def print_(ctx: ir.DefinitionContext):
            value = ctx.arg_value(0)
            value_type = ctx.arg_type(0)

            puts = ctx.c_registry.get_function('puts')

            ctx.builder.comment('converting value to string')
            value_str = ctx.call(f'{value_type}.to_string', [ir.CodegenArg(value_type, value)],
                                 'value_str')
            
            ctx.builder.comment('outputting value string')
            str_ptr = get_struct_field_value(ctx.builder, value_str, 0, 'value_str_ptr')
            ctx.builder.call(puts, [str_ptr])

            ctx.builder.comment('destroying string')
            ref_type = ctx.scope.type_map.get('Ref')
            ref_index = index_of_type(value_str.type, lir.PointerType(ref_type.type))
            ctx.call('Ref.dec', [ir.CodegenArg(ref_type, get_struct_field_value(
                ctx.builder, value_str, ref_index, 'value_str_ref'
            ))])
        
        @ir.builtin(self, params=[
            ir.Param(ir.Position.zero(), self.scope.type_map.get('string'), 'message')
        ])
        def err(ctx: ir.DefinitionContext):
            message = ctx.arg_value(0)

            puts = ctx.c_registry.get_function('puts')
            exit_ = ctx.c_registry.get_function('exit')

            str_ptr = get_struct_field_value(ctx.builder, message, 0, 'message_ptr')
            ctx.builder.call(puts, [str_ptr])
            ctx.builder.call(exit_, [lir.Constant(lir.IntType(32), 1)])
