from typing import Callable, Any, cast, TypeAlias, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import info

from llvmlite import ir as lir

from cure.codegen_utils import create_string_constant
from cure.c_registry import CRegistry
from cure import ir


LibraryType: TypeAlias = Union['Lib', 'LibType', 'Class']

def mangle_function_name(name: str, self: LibraryType):
    if isinstance(self, (Class, LibType)):
        return f'{self.type}.{name}'
    
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

        name = mangle_function_name(name or func.__name__, self)
        func.function = True
        func.name = name
        func.params = params
        func.ret_type = ret_type
        func.flags = flags
        func.self = self

        if self is not None:
            self.scope.symbol_table.add(ir.Symbol(
                name, cast(ir.Type, self.scope.type_map.get('function')), ir.Function(
                    ir.Position.zero(), ret_type, name, params, func, flags
                )
            ))
            
            setattr(self, name, func)
            info(f'Registered function {name} to {self.__class__.__name__}')
        
        return func
    
    return decorator

def overload(overload_of: Callable, params: list[ir.Param] | None = None,
             ret_type: ir.Type | None = None, name: str | None = None):
    if params is None:
        params = []
    
    if ret_type is None:
        ret_type = getattr(overload_of, 'self').scope.type_map.get('nil')
    
    def decorator(func):
        nonlocal name
        
        self = overload_of.self
        name = mangle_function_name(name or func.__name__, self)

        func.function = True
        func.name = name
        func.params = params
        func.ret_type = ret_type
        func.flags = overload_of.flags
        func.overload_of = overload_of

        if self is not None:
            base = self.scope.symbol_table.get(overload_of.name)
            if base is None:
                ir.Position.zero().comptime_error(
                    f'Failed to register overload {name}: base function does not'\
                        f'exist {overload_of.name}',
                    self.scope.src
                )
            
            base_func = base.value
            if not isinstance(base_func, ir.Function):
                ir.Position.zero().comptime_error(
                    f'Failed to register overload {name}: base function is not a function',
                    self.scope.src
                )
            
            base_func.overloads.append(ir.Function(
                ir.Position.zero(), ret_type, name, params, func, func.flags
            ))

            setattr(self, name, func)
            info(f'Registered overload {name} to {self.__class__.__name__}')
        
        return func
    
    return decorator

def getattrs(instance: LibraryType):
    attrs = {}
    for k in dir(instance):
        v = getattr(instance, k)
        if k.startswith('_') or not callable(v) or not getattr(v, 'function', False):
            continue

        attrs[k] = v
    
    return attrs


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
            ir.CallArgument(lir.Constant(lir.IntType(32), len(message)),
                         cast(ir.Type, self.scope.type_map.get('int')))
        ])

        self.call('error', [ir.CallArgument(
            err_string_struct, cast(ir.Type, self.scope.type_map.get('string'))
        )])
        
        info(f'Inserted error with message: {message}')
        self.builder.unreachable()

class Lib(ABC):
    def __init__(self, scope: ir.Scope):
        self.scope = scope
        self._name = type(self).__name__

        self.init()
    
    def init(self):
        ...

    def add(self, cls: type[LibraryType]):
        instance = cls(self.scope)
        info(f'Merged {self._name} and {instance._name} ({instance.__class__.__name__})')

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
