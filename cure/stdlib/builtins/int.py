from typing import override

from llvmlite import ir as lir

from cure.codegen_utils import create_static_buffer, create_string_constant
from cure import ir


class int(ir.Class):
    @override
    def init(self):
        BUF_SIZE = 16

        @ir.builtin(self, self.scope.type_map.get('string'), [
            ir.Param(ir.Position.zero(), self.type, 'i')
        ])
        def to_string(ctx: ir.DefinitionContext):
            i = ctx.arg_value(0)

            snprintf = ctx.c_registry.get_function('snprintf')
            strlen = ctx.c_registry.get_function('strlen')

            buf_size_const = lir.Constant(lir.IntType(64), BUF_SIZE)
            buf = create_static_buffer(
                ctx.module, lir.IntType(8), BUF_SIZE, ctx.module.get_unique_name('int_buf')
            )

            if 'int_fmt' in ctx.module.globals:
                fmt = ctx.module.get_global('int_fmt')
            else:
                fmt = create_string_constant(ctx.module, '%d', 'int_fmt')
            
            ctx.builder.call(snprintf, [buf, buf_size_const, fmt, i])
            return ctx.call('string.new', [
                ir.CodegenArg(self.scope.type_map.get('__i8*'), buf),
                ir.CodegenArg(self.scope.type_map.get('__i64'), ctx.builder.call(
                    strlen, [buf], 'length'
                ))
            ])
        
        @ir.builtin(self, self.type, [
            ir.Param(ir.Position.zero(), self.type, 'a'),
            ir.Param(ir.Position.zero(), self.type, 'b')
        ], override_name='add.int')
        def add_int(ctx: ir.DefinitionContext):
            a, b = ctx.arg_value(0), ctx.arg_value(1)
            return ctx.builder.add(a, b)
        
        @ir.builtin(self, self.type, [
            ir.Param(ir.Position.zero(), self.type, 'a'),
            ir.Param(ir.Position.zero(), self.type, 'b')
        ], override_name='sub.int')
        def sub_int(ctx: ir.DefinitionContext):
            a, b = ctx.arg_value(0), ctx.arg_value(1)
            return ctx.builder.sub(a, b)
        
        @ir.builtin(self, self.type, [
            ir.Param(ir.Position.zero(), self.type, 'a'),
            ir.Param(ir.Position.zero(), self.type, 'b')
        ], override_name='mul.int')
        def mul_int(ctx: ir.DefinitionContext):
            a, b = ctx.arg_value(0), ctx.arg_value(1)
            return ctx.builder.mul(a, b)
