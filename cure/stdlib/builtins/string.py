from typing import override

from llvmlite import ir as lir

from cure.codegen_utils import cast_value, create_struct_value, get_struct_field_value
from cure import ir


class string(ir.Class):
    @override
    def init(self):
        @ir.builtin(self, self.type, [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('__i8*'), 'ptr'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('__i64'), 'length')
        ])
        def new(ctx: ir.DefinitionContext):
            ptr, length = ctx.arg_value(0), ctx.arg_value(1)

            malloc = ctx.c_registry.get_function('malloc')
            memcpy = ctx.c_registry.get_function('memcpy')

            ctx.builder.comment('Allocate new string')
            length_i32 = cast_value(ctx.builder, length, lir.IntType(64), 'length_i32')
            length_add_one = ctx.builder.add(
                length_i32, lir.Constant(lir.IntType(64), 1), 'malloc_size'
            )
            dest = ctx.builder.call(malloc, [length_add_one], 'ptr')

            ctx.builder.comment('Copy contents from parameter i8*')
            ctx.builder.call(memcpy, [dest, ptr, length])

            ctx.builder.comment('Add null terminator')
            dest_ptr = ctx.builder.gep(dest, [length], True, 'last_char')
            ctx.builder.store(lir.Constant(lir.IntType(8), 0), dest_ptr)

            ctx.builder.comment('Create ref*')
            ref = ctx.call(
                'Ref.new', [ir.CodegenArg(self.scope.type_map.get('any'), dest)], 'ref'
            )

            ctx.builder.comment('Create struct')
            return create_struct_value(ctx.builder, self.type.type, [dest, length, ref])
        
        @ir.builtin(self, self.type, [ir.Param(ir.Position.zero(), self.type, 's')])
        def clone(ctx: ir.DefinitionContext):
            s = ctx.arg_value(0)

            ptr = get_struct_field_value(ctx.builder, s, 0, 'ptr')
            length = get_struct_field_value(ctx.builder, s, 1, 'length')
            return ctx.call('string.new', [
                ir.CodegenArg(ctx.scope.type_map.get('__i8*'), ptr),
                ir.CodegenArg(ctx.scope.type_map.get('__i64'), length)
            ])
        
        @ir.builtin(self, self.type, [ir.Param(ir.Position.zero(), self.type, 's')])
        def to_string(ctx: ir.DefinitionContext):
            return ctx.call('string.clone', [ir.CodegenArg(self.type, ctx.arg_value(0))])
        
        @ir.builtin(self, self.scope.type_map.get('int'), [
            ir.Param(ir.Position.zero(), self.type, 's')
        ], is_property=True)
        def length(ctx: ir.DefinitionContext):
            return cast_value(
                ctx.builder, get_struct_field_value(ctx.builder, ctx.arg_value(0), 1, 'length_i64'),
                self.scope.type_map.get('int').type, 'length'
            )
