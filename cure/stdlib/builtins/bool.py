from typing import override

from llvmlite import ir as lir

from cure.codegen_utils import create_string_constant
from cure import ir


class bool(ir.Class):
    @override
    def init(self):
        @ir.builtin(self, self.scope.type_map.get('string'), [
            ir.Param(ir.Position.zero(), self.type, 'b')
        ])
        def to_string(ctx: ir.DefinitionContext):
            if 'true_str' not in ctx.module.globals:
                true_str = create_string_constant(ctx.module, 'true', 'true_str')
            else:
                true_str = ctx.module.get_global('true_str')

            if 'false_str' not in ctx.module.globals:
                false_str = create_string_constant(ctx.module, 'false', 'false_str')
            else:
                false_str = ctx.module.get_global('false_str')
            
            b = ctx.arg_value(0)
            b_str = ctx.builder.select(b, true_str, false_str, 'b_str')
            b_length = ctx.builder.select(
                b, lir.Constant(lir.IntType(64), 4), lir.Constant(lir.IntType(64), 5), 'b_length'
            )

            return ctx.call('string.new', [
                ir.CodegenArg(self.scope.type_map.get('__i8*'), b_str),
                ir.CodegenArg(self.scope.type_map.get('__i64'), b_length)
            ])
