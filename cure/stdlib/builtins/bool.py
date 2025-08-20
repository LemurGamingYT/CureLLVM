from typing import cast

from llvmlite import ir as lir

from cure.ir import Param, Position, Type, FunctionFlags, CallArgument
from cure.codegen_utils import create_string_constant, create_ternary
from cure.lib import function, LibType, DefinitionContext


class bool(LibType):
    def init_type(self):
        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('bool'), 'b')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True)
        )
        def to_string(ctx: DefinitionContext):
            b = ctx.param_value('b')

            ptr = create_ternary(
                ctx.builder, b,
                create_string_constant(ctx.module, 'true'), create_string_constant(ctx.module, 'false')
            )

            length = create_ternary(
                ctx.builder, b, lir.Constant(lir.IntType(32), 4), lir.Constant(lir.IntType(32), 5)
            )

            return ctx.call('string.new', [
                CallArgument(ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(length, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('bool'), 'b')
        ], self.scope.type_map.get('bool'))
        def eq_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('==', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('bool'), 'b')
        ], self.scope.type_map.get('bool'))
        def neq_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('!=', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('bool'), 'b')
        ], self.scope.type_map.get('bool'))
        def and_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.and_(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('bool'), 'b')
        ], self.scope.type_map.get('bool'))
        def or_bool(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.or_(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('bool'), 'a')
        ], self.scope.type_map.get('bool'))
        def not_(ctx: DefinitionContext):
            a = ctx.param_value('a')
            return ctx.builder.not_(a)
