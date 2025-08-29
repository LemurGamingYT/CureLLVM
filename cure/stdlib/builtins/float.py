from typing import override

from llvmlite import ir as lir

from cure.codegen_utils import create_static_buffer, create_string_constant
from cure import ir


class float(ir.Class):
    @override
    def init(self):
        BUF_SIZE = 64

        @ir.builtin(self, self.scope.type_map.get('string'), [
            ir.Param(ir.Position.zero(), self.type, 'i')
        ])
        def to_string(ctx: ir.DefinitionContext):
            i = ctx.arg_value(0)

            snprintf = ctx.c_registry.get_function('snprintf')
            strlen = ctx.c_registry.get_function('strlen')

            buf_size_const = lir.Constant(lir.IntType(64), BUF_SIZE)
            buf = create_static_buffer(
                ctx.module, lir.IntType(8), BUF_SIZE, ctx.module.get_unique_name('float_buf')
            )

            if 'float_fmt' in ctx.module.globals:
                fmt = ctx.module.get_global('float_fmt')
            else:
                fmt = create_string_constant(ctx.module, '%f', 'float_fmt')
            
            ctx.builder.call(snprintf, [buf, buf_size_const, fmt, i], 'written')
            return ctx.call('string.new', [
                ir.CodegenArg(self.scope.type_map.get('__i8*'), buf),
                ir.CodegenArg(self.scope.type_map.get('__i64'), ctx.builder.call(
                    strlen, [buf], 'length'
                ))
            ])
        
        @ir.builtin(self, self.type, [
            ir.Param(ir.Position.zero(), self.type, 'a'),
            ir.Param(ir.Position.zero(), self.type, 'b')
        ], override_name='add.float')
        def add_float(ctx: ir.DefinitionContext):
            a, b = ctx.arg_value(0), ctx.arg_value(1)
            return ctx.builder.fadd(a, b)
        
        @ir.builtin(self, self.type, [
            ir.Param(ir.Position.zero(), self.type, 'a'),
            ir.Param(ir.Position.zero(), self.type, 'b')
        ], override_name='sub.float')
        def sub_float(ctx: ir.DefinitionContext):
            a, b = ctx.arg_value(0), ctx.arg_value(1)
            return ctx.builder.fsub(a, b)
        
        @ir.builtin(self, self.type, [
            ir.Param(ir.Position.zero(), self.type, 'a'),
            ir.Param(ir.Position.zero(), self.type, 'b')
        ], override_name='mul.float')
        def mul_float(ctx: ir.DefinitionContext):
            a, b = ctx.arg_value(0), ctx.arg_value(1)
            return ctx.builder.fmul(a, b)
