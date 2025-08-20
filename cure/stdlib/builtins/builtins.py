from typing import cast

from llvmlite import ir as lir

from cure.ir import Param, Position, FunctionFlags, Type, CallArgument
from cure.lib import function, overload, Lib, DefinitionContext
from cure.stdlib.builtins.float import float as floatType
from cure.stdlib.builtins.bool import bool as boolType
from cure.stdlib.builtins.classes.string import string
from cure.stdlib.builtins.int import int as intType
from cure.stdlib.builtins.classes.Math import Math
from cure.stdlib.builtins.classes.Ref import Ref
from cure.target import Target
from cure.codegen_utils import (
    get_struct_value_field, create_static_buffer, NULL_BYTE, cast_value, create_string_constant,
    index_of_type, get_struct_ptr_field
)


class builtins(Lib):
    def init_lib(self):
        self.add_lib(Ref)
        self.add_type(Math)
        self.add_type(string)
        self.add_type(intType)
        self.add_type(boolType)
        self.add_type(floatType)

        @function(self, [Param(Position.zero(), self.scope.type_map.get('string'), 'message')],
                flags=FunctionFlags(public=True))
        def error(ctx: DefinitionContext):
            exit = ctx.c_registry.get('exit')
            puts = ctx.c_registry.get('puts')

            message = ctx.param_value('message')

            ctx.builder.call(puts, [get_struct_value_field(ctx.builder, message, 0)])
            ctx.builder.call(exit, [lir.Constant(cast(Type, self.scope.type_map.get('int')).type, 1)])

        @function(self, [Param(Position.zero(), self.scope.type_map.get('any'), 'x')],
                flags=FunctionFlags(public=True))
        def print(ctx: DefinitionContext):
            puts = ctx.c_registry.get('puts')

            x = ctx.param('x')
            x_str = ctx.call(f'{x.type}.to_string', [CallArgument(x.value, x.type)])
            ctx.builder.call(puts, [get_struct_value_field(ctx.builder, x_str, 0)])

            # manually free the string
            # (because the CodeGeneration's memory management does not apply here)
            Ref_type = cast(Type, self.scope.type_map.get('Ref'))
            ref_index = index_of_type(x_str.type, Ref_type.type.as_pointer())
            ref = ctx.builder.load(get_struct_ptr_field(ctx.builder, x_str, ref_index)) if\
                isinstance(x_str.type, lir.PointerType) else\
                get_struct_value_field(ctx.builder, x_str, ref_index)
            ctx.call('Ref.dec', [CallArgument(ref, Ref_type.as_pointer())])

        @function(self, [Param(Position.zero(), self.scope.type_map.get('string'), 'x')],
                flags=FunctionFlags(public=True))
        def print_literal(ctx: DefinitionContext):
            printf = ctx.c_registry.get('printf')

            x = ctx.param_value('x')
            ctx.builder.call(printf, [get_struct_value_field(ctx.builder, x, 0)])
        
        @function(self, ret_type=self.scope.type_map.get('string'), flags=FunctionFlags(public=True))
        def input(ctx: DefinitionContext):
            strlen = ctx.c_registry.get('strlen')
            fgets = ctx.c_registry.get('fgets')

            INPUT_BUF_SIZE = 256

            buf = create_static_buffer(ctx.module, lir.IntType(8), INPUT_BUF_SIZE)
            size_const = lir.Constant(lir.IntType(32), INPUT_BUF_SIZE)

            if ctx.scope.target == Target.Windows:
                acrt_iob_func = ctx.c_registry.get('__acrt_iob_func')
                stdin = ctx.builder.call(acrt_iob_func, [lir.Constant(lir.IntType(32), 0)])
            else:
                stdin_ptr = ctx.c_registry.get_global('stdin')
                stdin = ctx.builder.load(stdin_ptr)
            
            ctx.builder.call(fgets, [buf, size_const, stdin])

            input_len = ctx.builder.call(strlen, [buf])
            len_minus_one = ctx.builder.sub(input_len, lir.Constant(lir.IntType(64), 1))
            last_char_ptr = ctx.builder.gep(buf, [len_minus_one])
            last_char = ctx.builder.load(last_char_ptr)
            newline_char = lir.Constant(lir.IntType(8), ord('\n'))
            is_newline = ctx.builder.icmp_signed('==', last_char, newline_char)
            with ctx.builder.if_then(is_newline):
                ctx.builder.store(NULL_BYTE(), last_char_ptr)
                input_len = ctx.builder.sub(input_len, lir.Constant(lir.IntType(64), 1))

            input_len_i32 = cast_value(
                ctx.builder, input_len, cast(Type, self.scope.type_map.get('int')).type
            )
            
            return ctx.call('string.new', [
                CallArgument(buf, cast(Type, self.scope.type_map.get('pointer'))),
                CallArgument(input_len_i32, cast(Type, self.scope.type_map.get('int')))
            ])
        
        @overload(input, [Param(Position.zero(), self.scope.type_map.get('string'), 'prompt')],
                self.scope.type_map.get('string'))
        def input_prompt(ctx: DefinitionContext):
            prompt = ctx.param_value('prompt')

            printf = ctx.c_registry.get('printf')

            fmt = create_string_constant(ctx.module, '%s')
            prompt_ptr = get_struct_value_field(ctx.builder, prompt, 0)
            ctx.builder.call(printf, [fmt, prompt_ptr])
            return ctx.call('input')
