from typing import cast

from llvmlite import ir as lir

from cure.codegen_utils import cast_value, create_static_buffer, create_string_constant, float_zero
from cure.ir import Param, Position, Type, FunctionFlags, CallArgument
from cure.lib import function, LibType, DefinitionContext


class float(LibType):
    def init_type(self):
        BUF_SIZE = 64

        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('float'), 'f')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True)
        )
        def to_string(ctx: DefinitionContext):
            buf_size = lir.Constant(lir.IntType(64), BUF_SIZE)

            snprintf = ctx.c_registry.get('snprintf')

            f = ctx.param_value('f')

            buf = create_static_buffer(ctx.module, lir.IntType(8), BUF_SIZE)
            fmt_ptr = create_string_constant(ctx.module, r'%f')
            ctx.builder.call(snprintf, [buf, buf_size, fmt_ptr, f])

            buf_size_i32 = cast_value(
                ctx.builder, buf_size, cast(Type, self.scope.type_map.get('int')).type
            )

            return ctx.call('string.new', [
                CallArgument(buf, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(buf_size_i32, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('float'), 'x')],
            self.scope.type_map.get('float')
        )
        def to_int(ctx: DefinitionContext):
            x = ctx.param_value('x')
            return cast_value(ctx.builder, x, cast(Type, self.scope.type_map.get('int')).type)
        

        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('float'))
        def add_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fadd(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('float'))
        def sub_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fsub(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('float'))
        def mul_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fmul(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('float'))
        def div_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            div_by_zero = ctx.builder.fcmp_ordered('==', b, float_zero())
            with ctx.builder.if_then(div_by_zero):
                ctx.error('division by zero')
            
            return ctx.builder.fdiv(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('float'))
        def mod_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            div_by_zero = ctx.builder.fcmp_ordered('==', b, float_zero())
            with ctx.builder.if_then(div_by_zero):
                ctx.error('modulo by zero')
            
            return ctx.builder.frem(a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('bool'))
        def eq_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('==', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('bool'))
        def neq_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('!=', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('bool'))
        def lt_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('<', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('bool'))
        def gt_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('>', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('bool'))
        def lte_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('<=', a, b)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('float'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('float'), 'b')
        ], self.scope.type_map.get('bool'))
        def gte_float(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            return ctx.builder.fcmp_ordered('>=', a, b)
