from typing import cast

from llvmlite import ir as lir

from cure.ir import Param, Position, FunctionFlags, Type
from cure.lib import function, LibType, DefinitionContext
from cure.codegen_utils import (
    set_struct_field, get_struct_ptr_field, NULL, get_type_size, cast_value, get_struct_ptr_field_value
)


class Ref(LibType):
    def init(self):
        @function(self, [
            Param(Position.zero(), self.scope.type_map.get('pointer'), 'data'),
            Param(Position.zero(), self.scope.type_map.get('free_fn'), 'destroy_fn')
        ], self.scope.type_map.get('Ref').as_pointer(), flags=FunctionFlags(static=True, method=True))
        def new(ctx: DefinitionContext):
            malloc = ctx.c_registry.get('malloc')

            data = ctx.param_value('data')
            destroy_fn = ctx.param_value('destroy_fn')

            ctx.builder.comment('loading Ref struct size')
            ref_type = cast(Type, ctx.scope.type_map.get('Ref'))
            struct_size = get_type_size(ctx.builder, ref_type.type, 'Ref_size')

            ctx.builder.comment('allocating (dynamically) Ref struct')
            ptr = cast_value(
                ctx.builder,
                ctx.builder.call(malloc, [struct_size], 'raw_Ref'), 
                ref_type.type.as_pointer(),
                'Ref_struct'
            )

            free_fn = cast(Type, ctx.scope.type_map.get('free_fn'))
            destroy_fn = ctx.builder.bitcast(destroy_fn, free_fn.type, 'destroy_fn')
            
            ctx.builder.comment('setting Ref struct fields')
            set_struct_field(ctx.builder, ptr, 0, data, 'data')
            set_struct_field(ctx.builder, ptr, 1, destroy_fn, 'destroy_fn')
            set_struct_field(ctx.builder, ptr, 2, lir.Constant(lir.IntType(64), 1), 'ref_count')
            return ptr
        
        @function(self, [Param(Position.zero(), self.scope.type_map.get('Ref').as_pointer(), 'self')],
                flags=FunctionFlags(method=True))
        def inc(ctx: DefinitionContext):
            self = ctx.param_value('self')

            ctx.builder.comment('loading ref count')
            ref_count_ptr = get_struct_ptr_field(ctx.builder, self, 2, 'ref_count_ptr')
            ref_count = ctx.builder.load(ref_count_ptr, 'ref_count')

            ctx.builder.comment('adding one and storing new ref count')
            one = lir.Constant(lir.IntType(64), 1)
            new_count = ctx.builder.add(ref_count, one, 'incremented_ref_count')
            ctx.builder.store(new_count, ref_count_ptr)
        
        @function(self, [Param(Position.zero(), self.scope.type_map.get('Ref').as_pointer(), 'self')],
                flags=FunctionFlags(method=True))
        def dec(ctx: DefinitionContext):
            self = ctx.param_value('self')

            ctx.builder.comment('loading ref count')
            ref_count_ptr = get_struct_ptr_field(ctx.builder, self, 2, 'ref_count_ptr')
            ref_count = ctx.builder.load(ref_count_ptr, 'ref_count')

            ctx.builder.comment('subtracting one and storing new ref count')
            one = lir.Constant(lir.IntType(64), 1)
            new_count = ctx.builder.sub(ref_count, one, 'decremented_ref_count')
            ctx.builder.store(new_count, ref_count_ptr)

            ctx.builder.comment('checking if ref count is zero')
            zero = lir.Constant(lir.IntType(64), 0)
            with ctx.builder.if_then(ctx.builder.icmp_signed('==', new_count, zero, 'is_null')):
                ctx.builder.comment('ref count is zero')
                free = ctx.c_registry.get('free')

                ctx.builder.comment('loading data')
                data_ptr_ptr = get_struct_ptr_field(ctx.builder, self, 0)
                data_ptr = ctx.builder.load(data_ptr_ptr)
                
                ctx.builder.comment('loading destroy function')
                destroy_fn = get_struct_ptr_field_value(ctx.builder, self, 1, 'destroy_fn')
                
                func_ptr_type = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer()
                ]).as_pointer()
                null_func_ptr = lir.Constant(func_ptr_type, None)
                
                ctx.builder.comment('checking if the destroy function is NULL')
                with ctx.builder.if_else(ctx.builder.icmp_signed('!=', destroy_fn, null_func_ptr))\
                    as (then, else_):
                    with then:
                        ctx.builder.comment('calling destroy function')
                        ctx.builder.call(destroy_fn, [data_ptr])
                    
                    with else_:
                        ctx.builder.comment('calling default destroy function (free)')
                        ctx.builder.call(free, [data_ptr])
                
                ctx.builder.comment('set data pointer to NULL')
                ctx.builder.store(NULL(), data_ptr_ptr)

                ctx.builder.comment('freeing Ref struct')
                ctx.builder.call(free, [cast_value(ctx.builder, self, lir.IntType(8).as_pointer())])
