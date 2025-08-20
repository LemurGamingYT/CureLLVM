from typing import cast

from llvmlite import ir as lir

from cure.codegen_utils import cast_value, create_static_buffer, create_string_constant, zero
from cure.ir import Param, Position, Type, FunctionFlags, CallArgument
from cure.lib import function, LibType, DefinitionContext


class int(LibType):
    def init_type(self):
        BUF_SIZE = 16

        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('int'), 'i')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True)
        )
        def to_string(ctx: DefinitionContext):
            buf_size = lir.Constant(lir.IntType(64), BUF_SIZE)

            snprintf = ctx.c_registry.get('snprintf')

            x = ctx.param_value(0)

            buf = create_static_buffer(ctx.module, lir.IntType(8), BUF_SIZE)
            fmt_ptr = create_string_constant(ctx.module, r'%d')
            ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, x])

            buf_size_i32 = cast_value(
                ctx.builder, buf_size, cast(Type, self.scope.type_map.get('int')).type
            )

            return ctx.call('string.new', [
                CallArgument(buf, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(buf_size_i32, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('int'), 'x')],
            self.scope.type_map.get('float')
        )
        def to_float(ctx: DefinitionContext):
            x = ctx.param_value('x')
            return cast_value(ctx.builder, x, cast(Type, self.scope.type_map.get('float')).type)
        

        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('int'))
        def add_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.add(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('int'))
        def sub_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.sub(a, b)

        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('int'))
        def mul_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.mul(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('int'))
        def div_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            div_by_zero = ctx.builder.icmp_signed('==', b, zero(32))
            with ctx.builder.if_then(div_by_zero):
                ctx.error('division by zero')
            
            return ctx.builder.sdiv(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('int'))
        def mod_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            div_by_zero = ctx.builder.icmp_signed('==', b, zero(32))
            with ctx.builder.if_then(div_by_zero):
                ctx.error('modulo by zero')
            
            return ctx.builder.srem(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('bool'))
        def eq_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('==', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('bool'))
        def neq_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('!=', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('bool'))
        def lt_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('<', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('bool'))
        def gt_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('>', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('bool'))
        def lte_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('<=', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('int'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'b')
        ], self.scope.type_map.get('bool'))
        def gte_int(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.icmp_signed('>=', a, b)
