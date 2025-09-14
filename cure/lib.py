from typing import Callable, Any, cast, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import info, debug

from llvmlite import ir as lir

from cure.codegen_utils import create_string_constant
from cure.c_registry import CRegistry
from cure import ir


def get_method_name(self, name: str):
    if isinstance(self, (Class, LibType)) and not name.startswith(f'{self.type}.'):
        return f'{self.type}.{name}'
    else:
        return name

def function(self: Any, params: list[ir.Param] | None = None, ret_type: ir.Type | None = None,
             flags: ir.FunctionFlags | None = None, name: str | None = None):
    if params is None:
        params = []
    
    if ret_type is None:
        ret_type = self.scope.type_map.get('nil')
    
    if flags is None:
        flags = ir.FunctionFlags()
    
    def decorator(func):
        nonlocal name

        name = get_method_name(self, name or func.__name__)

        func.function = True
        func.name = name
        func.params = params
        func.ret_type = ret_type
        func.flags = flags
        func.overloads = []
        func.self = self

        if self is not None:
            setattr(self, name, func)

            self.scope.symbol_table.add(ir.Symbol(
                name, self.scope.type_map.get('function'), ir.Function(
                    ir.Position.zero(), ret_type, name, params, func, flags, func.overloads
                )
            ))

            info(f'Registered function {name}')
        
        return func
    
    return decorator

def overload(overload_of: Callable, params: list[ir.Param] | None = None,
             ret_type: ir.Type | None = None, name: str | None = None):
    self = getattr(overload_of, 'self')
    if params is None:
        params = []
    
    if ret_type is None:
        ret_type = self.scope.type_map.get('nil')
    
    def decorator(func):
        nonlocal name
        
        name = get_method_name(self, name or func.__name__)

        func.function = True
        func.name = name
        func.params = params
        func.ret_type = ret_type
        func.flags = overload_of.flags
        func.overload_of = overload_of

        if self is not None:
            overload_of.overloads.append(ir.Function(
                ir.Position.zero(), ret_type, name, params, func, func.flags
            ))

            info(f'Registered overload {name} (overload of {overload_of.name})')
        
        return func
    
    return decorator

def getattrs(instance):
    attrs = {}
    for k in dir(instance):
        v = getattr(instance, k)
        if k.startswith('_') or not callable(v) or not getattr(v, 'function', False):
            continue

        attrs[k] = v
    
    return attrs

def add_instance(self, instance):
    attrs = [attr.__name__ for attr in getattrs(instance).values()]
    debug(f'Adding {attrs} (from instance {instance}) to {self}')

    for v in getattrs(instance).values():
        if (overload_of := getattr(v, 'overload_of', None)) is not None:
            overload(overload_of, v.params, v.ret_type, v.name)(v)
        else:
            function(self, v.params, v.ret_type, v.flags, v.name)(v)

        info(f'Added {v.name} from {self._name}')


@dataclass
class ParamPointer:
    value: lir.Value
    type: ir.Type

@dataclass
class DefinitionContext:
    pos: ir.Position
    scope: ir.Scope
    module: lir.Module
    builder: lir.IRBuilder
    c_registry: CRegistry
    params: list[ir.Param]
    ret_type: ir.Type

    def param(self, name_or_index: str | int) -> ParamPointer:
        if isinstance(name_or_index, int):
            if name_or_index >= len(self.params):
                return self.pos.comptime_error(f'invalid param index {name_or_index}', self.scope.src)
            
            param = self.params[name_or_index]
            name = param.name
        else:
            name = name_or_index
        
        for param in self.params:
            if param.name != name:
                continue

            symbol = self.scope.symbol_table.get(name)
            if symbol is None:
                return self.pos.comptime_error(f'invalid param {name}', self.scope.src)
            
            value = symbol.value
            if isinstance(symbol.value, lir.PointerType):
                value = self.builder.load(value, symbol.name)
            
            return ParamPointer(value, symbol.type)

        return self.pos.comptime_error(f'unknown param {name}', self.scope.src)
    
    def param_value(self, name_or_index: str | int) -> lir.Value:
        return self.param(name_or_index).value
    
    def call(self, name: str, args: list[ir.CallArgument] | None = None):
        return self.scope.call(self.pos, self.builder, self.module, name, args)
    
    def error(self, message: str):
        err_msg = create_string_constant(self.module, message)
        err_string_struct = self.call('string.new', [
            ir.CallArgument(err_msg, cast(ir.Type, self.scope.type_map.get('pointer'))),
            ir.CallArgument(
                lir.Constant(lir.IntType(32), len(message)),
                cast(ir.Type, self.scope.type_map.get('int'))
            )
        ])

        self.call('error', [ir.CallArgument(
            err_string_struct, cast(ir.Type, self.scope.type_map.get('string'))
        )])
        
        self.builder.unreachable()

class Lib(ABC):
    def __init__(self, scope: ir.Scope):
        self.scope = scope
        self._name = type(self).__name__

        self.init()
    
    def init(self):
        ...

    def add(self, cls: type[Union['Lib', 'Class']]):
        instance = cls(self.scope)
        add_instance(self, instance)
        info(f'merged {self._name} and {instance._name} (Lib)')

@dataclass
class LibType:
    def __init__(self, scope: ir.Scope):
        self.scope = scope

        self._name = type(self).__name__
        self.type = self.scope.type_map.get(self._name)
        if self.type is None:
            ir.Position.zero().comptime_error(f'unknown type {self._name}', scope.src)

        self.init()
    
    def init(self):
        ...

@dataclass
class ClassField:
    name: str
    type: ir.Type

class Class(ABC):
    @abstractmethod
    def fields(self) -> list[ClassField]:
        ...

    def __init__(self, scope: ir.Scope, *generic_types: ir.Type):
        self.generic_types = generic_types
        self.scope = scope

        self._class_name = type(self).__name__
        if not hasattr(self, '_name'):
            self._name = self._class_name + ''.join(f'_{type}' for type in generic_types)

        if not self.scope.type_map.has(self._name):
            self.scope.type_map.add(self._name, self._create_struct())
        
        if not hasattr(self, 'type'):
            self.type = self.scope.type_map.get(self._name)

        self.init()
    
    def _create_struct(self):
        struct_type = lir.global_context.get_identified_type(self._name)
        if struct_type.is_opaque:
            struct_type.set_body(*[field.type.type for field in self.fields()])
        
        return struct_type
    
    def init(self):
        ...
