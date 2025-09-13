from typing import cast

from llvmlite import ir as lir

from cure.ir import Param, Position, Type, FunctionFlags, CallArgument
from cure.lib import function, LibType, DefinitionContext
from cure.codegen_utils import (
    get_struct_value_field, create_struct_value, cast_value, NULL_BYTE, zero, NULL,
    get_struct_ptr_field, get_struct_ptr_field_value
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

            ctx.builder.comment('allocating (dynamically) string data +1 size for the null terminator')
            one = lir.Constant(lir.IntType(64), 1)
            tot_length = ctx.builder.add(length, one)
            data_ptr = cast_value(
                ctx.builder,
                ctx.builder.call(malloc, [tot_length], 'raw_data'),
                lir.IntType(8).as_pointer(),
                'data_ptr'
            )

            ctx.builder.comment('copying string data')
            ctx.builder.call(memcpy, [data_ptr, literal, length])

            ctx.builder.comment('storing \\0 byte at the end of string data')
            null_ptr = ctx.builder.gep(data_ptr, [length], 'last_char_ptr')
            ctx.builder.store(NULL_BYTE(), null_ptr)

            free_fn = cast(Type, ctx.scope.type_map.get('free_fn'))
            null_func_ptr = lir.Constant(free_fn.type, None)
            
            ref = ctx.call('Ref.new', [
                CallArgument(data_ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(null_func_ptr, free_fn)
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

            length = get_struct_value_field(ctx.builder, s, 1, 'length')
            return cast_value(ctx.builder, length, cast(Type, self.scope.type_map.get('int')).type)
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 's'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'index')
        ], self.scope.type_map.get('string'), flags=FunctionFlags(method=True))
        def get(ctx: DefinitionContext):
            s = ctx.param_value('s')
            index = ctx.param_value('index')

            ctx.builder.comment('loading string length')
            length = get_struct_value_field(ctx.builder, s, 1, 'length')
            length_i32 = cast_value(ctx.builder, length, lir.IntType(32), 'length_i32')
            
            ctx.builder.comment('wrapping negative index')
            is_neg_idx = ctx.builder.icmp_signed('<', index, zero(32), 'is_negative_index')
            with ctx.builder.if_then(is_neg_idx):
                index = ctx.builder.add(length_i32, index)
            
            ctx.builder.comment('checking if index is out of bounds')
            index_oob = ctx.builder.icmp_signed('>', index, length_i32, 'index_out_of_bounds')
            with ctx.builder.if_then(index_oob):
                ctx.error('string index out of bounds')

            ptr = get_struct_value_field(ctx.builder, s, 0, 'ptr')
            index_ptr = ctx.builder.gep(ptr, [index], 'index_ptr')
            return ctx.call('string.new', [
                CallArgument(index_ptr, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(length_i32, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 's')
        ], self.scope.type_map.get('int'), flags=FunctionFlags(method=True))
        def parse_int(ctx: DefinitionContext):
            s = ctx.param_value('s')

            strtol = ctx.c_registry.get('strtol')

            base = lir.Constant(lir.IntType(32), 10)
            ptr = get_struct_value_field(ctx.builder, s, 0, 'ptr')
            return cast_value(
                ctx.builder, ctx.builder.call(strtol, [ptr, NULL(), base], 'parsed_int'),
                cast(Type, self.scope.type_map.get('int')).type
            )
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 's')
        ], self.scope.type_map.get('float'), flags=FunctionFlags(method=True))
        def parse_float(ctx: DefinitionContext):
            s = ctx.param_value('s')

            strtod = ctx.c_registry.get('strtod')

            ptr = get_struct_value_field(ctx.builder, s, 0, 'ptr')
            return cast_value(
                ctx.builder, ctx.builder.call(strtod, [ptr, NULL()], 'parsed_float'),
                cast(Type, self.scope.type_map.get('float')).type
            )
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string').as_reference(), 's'),
            Param(Position.zero(), self.scope.type_map.get('int'), 'index'),
            Param(Position.zero(), self.scope.type_map.get('string'), 'value')
        ], flags=FunctionFlags(method=True))
        def set(ctx: DefinitionContext):
            s = ctx.param_value('s')
            index = ctx.param_value('index')
            value = ctx.param_value('value')

            ctx.builder.comment('loading string length')
            length = get_struct_ptr_field_value(ctx.builder, s, 1, 'length')
            length_i32 = cast_value(ctx.builder, length, lir.IntType(32), 'length_i32')

            ctx.builder.comment('wrapping negative index')
            is_neg_idx = ctx.builder.icmp_signed('<', index, zero(32), 'is_negative_index')
            with ctx.builder.if_then(is_neg_idx):
                index = ctx.builder.add(length_i32, index)
            
            ctx.builder.comment('checking if index is out of bounds')
            index_oob = ctx.builder.icmp_signed('>', index, length_i32, 'index_out_of_bounds')
            with ctx.builder.if_then(index_oob):
                ctx.error('string index out of bounds')
            
            ptr = get_struct_ptr_field(ctx.builder, s, 0, 'ptr')
            index_ptr = ctx.builder.gep(ptr, [index], 'index_ptr')

            value_ptr = get_struct_value_field(ctx.builder, value, 0, 'ptr')
            ctx.builder.store(value_ptr, index_ptr)


        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('string'), 'b')
        ], self.scope.type_map.get('string'))
        def add_string(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')

            memcpy = ctx.c_registry.get('memcpy')
            malloc = ctx.c_registry.get('malloc')

            ctx.builder.comment('calculating total length')
            a_len = get_struct_value_field(ctx.builder, a, 1, 'a_length')
            b_len = get_struct_value_field(ctx.builder, b, 1, 'b_length')
            total_length = ctx.builder.add(a_len, b_len, 'tot_length')

            ctx.builder.comment('allocating string data +1 size for the null terminator')
            ptr = ctx.builder.call(malloc, [ctx.builder.add(
                total_length, lir.Constant(lir.IntType(64), 1)
            )], 'ptr')

            ctx.builder.comment('copying string a data to the new string data')
            a_buf = get_struct_value_field(ctx.builder, a, 0, 'a_ptr')
            b_buf = get_struct_value_field(ctx.builder, b, 0, 'b_ptr')
            ctx.builder.call(memcpy, [ptr, a_buf, a_len])

            ctx.builder.comment('copying string b data to the new string data')
            ptr_offset = ctx.builder.gep(ptr, [a_len], 'ptr_offset')
            ctx.builder.call(memcpy, [ptr_offset, b_buf, b_len])

            ctx.builder.comment('storing \\0 byte at the end of string data')
            null_pos = ctx.builder.gep(ptr, [total_length], 'null_pos')
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

            a_len = get_struct_value_field(ctx.builder, a, 1, 'a_len')
            b_len = get_struct_value_field(ctx.builder, b, 1, 'b_len')

            ctx.builder.comment('checking if lengths do not match')
            with ctx.builder.if_then(ctx.builder.icmp_signed('!=', a_len, b_len, 'lengths_match')):
                ctx.builder.ret(zero(0)) # false

            ctx.builder.comment('checking is pointers are equal')
            a_ptr = get_struct_value_field(ctx.builder, a, 0, 'a_ptr')
            b_ptr = get_struct_value_field(ctx.builder, b, 0, 'b_ptr')
            return ctx.builder.icmp_signed(
                '==',
                ctx.builder.call(memcmp, [a_ptr, b_ptr, a_len]),
                zero(0)
            )
        
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('string'), 'a'),
            Param(Position.zero(), self.scope.type_map.get('string'), 'b')
        ], self.scope.type_map.get('bool'))
        def neq_string(ctx: DefinitionContext):
            a = ctx.param_value('a')
            b = ctx.param_value('b')
            
            memcmp = ctx.c_registry.get('memcmp')

            a_len = get_struct_value_field(ctx.builder, a, 1, 'a_len')
            b_len = get_struct_value_field(ctx.builder, b, 1, 'b_len')

            ctx.builder.comment('checking if lengths match')
            with ctx.builder.if_then(ctx.builder.icmp_signed('==', a_len, b_len, 'lengths_match')):
                ctx.builder.ret(zero(0)) # false

            ctx.builder.comment('checking is pointers are equal')
            a_ptr = get_struct_value_field(ctx.builder, a, 0, 'a_ptr')
            b_ptr = get_struct_value_field(ctx.builder, b, 0, 'b_ptr')
            return ctx.builder.icmp_signed(
                '!=',
                ctx.builder.call(memcmp, [a_ptr, b_ptr, a_len]),
                zero(0)
            )
