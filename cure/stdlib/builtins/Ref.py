from typing import override

from llvmlite import ir as lir

from cure.codegen_utils import get_type_size, cast_value, set_struct_field, get_struct_field_value
from cure import ir


class Ref(ir.Class):
    @override
    def init(self):
        @ir.builtin(self, self.type.as_pointer(), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('any'), 'data')
        ])
        def new(ctx: ir.DefinitionContext):
            data = ctx.arg_value(0)

            malloc = ctx.c_registry.get_function('malloc')

            ref_type = self.type.type
            ref_ptr = ctx.builder.call(malloc, [get_type_size(ctx.builder, ref_type, 'ref_size')])
            ref = cast_value(ctx.builder, ref_ptr, lir.PointerType(ref_type), 'ref_ptr')
            set_struct_field(ctx.builder, ref, 0, data)
            set_struct_field(ctx.builder, ref, 1, lir.Constant(lir.IntType(64), 1))
            return ref
        
        @ir.builtin(self, self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.type.as_pointer(), 'ref')
        ])
        def dec(ctx: ir.DefinitionContext):
            ref = ctx.arg_value(0)

            free = ctx.c_registry.get_function('free')

            ctx.builder.comment('Decrement ref count')
            set_struct_field(ctx.builder, ref, 1, ctx.builder.sub(
                get_struct_field_value(ctx.builder, ref, 1, 'ref_count'),
                lir.Constant(lir.IntType(64), 1)
            ))

            ctx.builder.comment('Free if ref count is zero')
            ref_count = get_struct_field_value(ctx.builder, ref, 1, 'ref_count')
            ref_count_is_zero = ctx.builder.icmp_signed(
                '==', ref_count, lir.Constant(lir.IntType(64), 0)
            )
            with ctx.builder.if_then(ref_count_is_zero):
                ctx.builder.call(free, [get_struct_field_value(ctx.builder, ref, 0, 'data')])
                ctx.builder.call(free, [cast_value(
                    ctx.builder, ref, lir.PointerType(lir.IntType(8))
                )])
        
        @ir.builtin(self, self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.type.as_pointer(), 'ref')
        ])
        def inc(ctx: ir.DefinitionContext):
            ref = ctx.arg_value(0)

            set_struct_field(ctx.builder, ref, 1, ctx.builder.add(
                get_struct_field_value(ctx.builder, ref, 1, 'ref_count'),
                lir.Constant(lir.IntType(64), 1)
            ))
