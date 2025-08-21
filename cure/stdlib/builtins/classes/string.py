from typing import cast

from llvmlite import ir as lir

from cure.ir import Param, Position, Type, FunctionFlags, CallArgument
from cure.lib import function, LibType, DefinitionContext
from cure.codegen_utils import (
    get_struct_value_field, create_struct_value, cast_value, NULL_BYTE, zero, NULL
)


class string(LibType):
    def init(self):
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('pointer'), 'literal'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'length')
        ], self.scope.type_map.get('string'), flags=FunctionFlags(method=True))
        def new(ctx: DefinitionContext):
            literal = ctx.param_value('literal')

            length = cast_value(ctx.builder, ctx.param_value('length'), lir.IntType(64))
            string_type = cast(Type, self.scope.type_map.get('string')).type

            malloc = ctx.c_registry.get('malloc')
            memcpy = ctx.c_registry.get('memcpy')

            # +1 for null terminator
            one = lir.Constant(lir.IntType(64), 1)
            tot_length = ctx.builder.add(length, one)
            data_ptr = ctx.builder.bitcast(
                ctx.builder.call(malloc, [tot_length]),
                lir.PointerType(lir.IntType(8))
            )
            ctx.builder.call(memcpy, [data_ptr, literal, length])

            null_ptr = ctx.builder.gep(data_ptr, [length])
            ctx.builder.store(NULL_BYTE(), null_ptr)

            func_ptr_type = lir.PointerType(lir.FunctionType(
                lir.PointerType(lir.IntType(8)), [lir.PointerType(lir.IntType(8))]
            ))
            null_func_ptr = lir.Constant(func_ptr_type, None)
            
            ref = ctx.call('Ref.new', [
                CallArgument(data_ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(null_func_ptr, cast(Type, self.scope.type_map.get('any_function')))
            ])

            return create_struct_value(ctx.builder, string_type, [data_ptr, length, ref])
        
        
        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('string'), 'x')],
            self.scope.type_map.get('string'), flags=FunctionFlags(method=True),
        )
        def to_string(ctx: DefinitionContext):
            return ctx.param_value('x')

        @function(
            self, [Param(Position.zero(), self.scope.type_map.get('string'), 's')],
            self.scope.type_map.get('int'), flags=FunctionFlags(property=True)
        )
        def length(ctx: DefinitionContext):
            s = ctx.param_value('s')

            length = get_struct_value_field(ctx.builder, s, 1)
            return cast_value(ctx.builder, length, cast(Type, self.scope.type_map.get('int')).type)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 's'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'index')
        ], self.scope.type_map.get('string'), flags=FunctionFlags(method=True))
        def get(ctx: DefinitionContext):
            s = ctx.param_value('s')
            index = ctx.param_value('index')

            length = get_struct_value_field(ctx.builder, s, 1)
            length_i32 = cast_value(ctx.builder, length, lir.IntType(32))
            with ctx.builder.if_then(ctx.builder.icmp_signed('>', index, length_i32)):
                ctx.error('string index out of bounds')
            
            with ctx.builder.if_then(ctx.builder.icmp_signed('<', index, zero(32))):
                index = ctx.builder.add(length_i32, index)

            ptr = get_struct_value_field(ctx.builder, s, 0)
            index_ptr = ctx.builder.gep(ptr, [index])
            return ctx.call('string.new', [
                CallArgument(index_ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(lir.Constant(lir.IntType(32), 1),
                             cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 's')
        ], self.scope.type_map.get('int'), flags=FunctionFlags(method=True))
        def parse_int(ctx: DefinitionContext):
            s = ctx.param_value('s')

            strtol = ctx.c_registry.get('strtol')

            base = lir.Constant(lir.IntType(32), 10)
            ptr = get_struct_value_field(ctx.builder, s, 0)
            return cast_value(
                ctx.builder, ctx.builder.call(strtol, [ptr, NULL(), base]),
                cast(Type, self.scope.type_map.get('int')).type
            )
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 's')
        ], self.scope.type_map.get('float'), flags=FunctionFlags(method=True))
        def parse_float(ctx: DefinitionContext):
            s = ctx.param_value('s')

            strtod = ctx.c_registry.get('strtod')

            ptr = get_struct_value_field(ctx.builder, s, 0)
            return cast_value(
                ctx.builder, ctx.builder.call(strtod, [ptr, NULL()]),
                cast(Type, self.scope.type_map.get('float')).type
            )
        

        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('string'), 'b')
        ], self.scope.type_map.get('string'))
        def add_string(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            memcpy = ctx.c_registry.get('memcpy')
            malloc = ctx.c_registry.get('malloc')

            a_len = get_struct_value_field(ctx.builder, a, 1)
            b_len = get_struct_value_field(ctx.builder, b, 1)
            total_length = ctx.builder.add(a_len, b_len)
            ptr = ctx.builder.call(malloc, [ctx.builder.add(
                total_length, lir.Constant(lir.IntType(64), 1)
            )])

            a_buf = get_struct_value_field(ctx.builder, a, 0)
            b_buf = get_struct_value_field(ctx.builder, b, 0)
            ctx.builder.call(memcpy, [ptr, a_buf, a_len])

            ptr_offset = ctx.builder.gep(ptr, [a_len])
            ctx.builder.call(memcpy, [ptr_offset, b_buf, b_len])

            null_pos = ctx.builder.gep(ptr, [total_length])
            null_byte = lir.Constant(lir.IntType(8), 0)
            ctx.builder.store(null_byte, null_pos)
            
            total_length_i32 = cast_value(
                ctx.builder, total_length, cast(Type, self.scope.type_map.get('int')).type
            )
            return ctx.call('string.new', [
                CallArgument(ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(total_length_i32, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('string'), 'b')
        ], self.scope.type_map.get('bool'))
        def eq_string(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            
            memcmp = ctx.c_registry.get('memcmp')

            a_len = get_struct_value_field(ctx.builder, a, 1)
            b_len = get_struct_value_field(ctx.builder, b, 1)
            with ctx.builder.if_then(ctx.builder.icmp_signed('!=', a_len, b_len)):
                ctx.builder.ret(zero(1))
            
            a_ptr = get_struct_value_field(ctx.builder, a, 0)
            b_ptr = get_struct_value_field(ctx.builder, b, 0)
            return ctx.builder.icmp_signed(
                '==',
                ctx.builder.call(memcmp, [a_ptr, b_ptr, a_len]),
                zero(1)
            )
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('string'), 'b')
        ], self.scope.type_map.get('bool'))
        def neq_string(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            
            memcmp = ctx.c_registry.get('memcmp')

            a_len = get_struct_value_field(ctx.builder, a, 1)
            b_len = get_struct_value_field(ctx.builder, b, 1)
            with ctx.builder.if_then(ctx.builder.icmp_signed('==', a_len, b_len)):
                ctx.builder.ret(zero(1))
            
            a_ptr = get_struct_value_field(ctx.builder, a, 0)
            b_ptr = get_struct_value_field(ctx.builder, b, 0)
            return ctx.builder.icmp_signed(
                '!=',
                ctx.builder.call(memcmp, [a_ptr, b_ptr, a_len]),
                zero(1)
            )
