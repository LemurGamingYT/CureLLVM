from typing import Union, Any, Callable, Optional
from dataclasses import dataclass, field
from importlib import import_module
from abc import ABC, abstractmethod
from sys import exit as sys_exit
from logging import error, info
from subprocess import run
from pathlib import Path

from llvmlite import ir as lir, binding
from colorama import Fore, Style

from cure.codegen_utils import create_string_constant, index_of_type, get_struct_field_value


node_kwargs = {'frozen': True}
STDLIB_PATH = Path(__file__).parent / 'stdlib'
op_map = {'+': 'add', '-': 'sub', '*': 'mul'}

def run_function(scope: 'Scope', callee: str, args: list['CodegenArg'], name: str = ''):
    symbol = scope.symbol_table.get(callee)
    if symbol is None:
        raise RuntimeError(f'{callee} could not be called')
    
    func = symbol.value
    if isinstance(func, lir.Function):
        ir_func = func
    elif isinstance(func, Function) and len(func.generic_params) == 0:
        ir_func = func.codegen(scope)
    elif isinstance(func, Function) and len(func.generic_params) > 0:
        ir_func = func.codegen(scope, args)
    
    return scope.builder.call(ir_func, [arg.value for arg in args], name)

@dataclass
class Position:
    line: int
    column: int
    
    @staticmethod
    def zero():
        return Position(0, 0)

    def comptime_error(self, scope: 'Scope', message: str):
        error_message_prefix = f'error in {scope.file.name}'
        if self.line != 0 and self.column != 0 and scope.file.is_file():
            src = scope.file.read_text()
            print(src.splitlines()[self.line - 1])
            print(' ' * self.column + '^')

            error_message_prefix = f'error in {scope.file.name}:{self.line}'
        
        print(f'{Style.BRIGHT}{Fore.RED}{error_message_prefix}: {message}{Style.RESET_ALL}')
        error(message)
        sys_exit(1)

@dataclass
class Symbol:
    name: str
    type: 'Type'
    value: Any
    is_mutable: bool = False

@dataclass
class SymbolTable:
    symbols: dict[str, Symbol] = field(default_factory=dict)
    local_symbols: dict[str, Symbol] = field(default_factory=dict)

    def get(self, name: str):
        return self.local_symbols.get(name) or self.symbols.get(name)
                 
    def add(self, symbol: Symbol):
        self.symbols[symbol.name] = symbol
        self.local_symbols[symbol.name] = symbol
    
    def has(self, name: str):
        return name in self.local_symbols or name in self.symbols
                 
    def remove(self, name: str):
        if name in self.local_symbols:
            del self.local_symbols[name]
        
        if name in self.symbols:
            del self.symbols[name]
    
    def clone(self):
        return SymbolTable(self.symbols.copy())
    
    def merge(self, other: 'SymbolTable'):
        self.symbols.update(other.symbols)
                 
@dataclass
class TypeMap:
    types: dict[str, 'Type'] = field(default_factory=dict)
                 
    def get(self, name: str):
        return self.types.get(name)
                 
    def add(self, display: str, type: lir.Type):
        self.types[display] = Type(Position.zero(), type, display)

        info(f'Added type \'{display}\' to the Type Map')
    
    def has(self, name: str):
        return name in self.types
                 
    def remove(self, name: str):
        if self.has(name):
            del self.types[name]
    
    def clone(self):
        return TypeMap(self.types.copy())
    
    def merge(self, other: 'TypeMap'):
        self.types.update(other.types)

class CRegistry:
    def __init__(self, module: lir.Module):
        self.registered_functions: dict[str, lir.FunctionType] = {}

        self.module = module
    
    def register_function(self, name: str, signature: lir.FunctionType):
        self.registered_functions[name] = signature
    
    def get_function(self, name: str):
        if name in self.module.globals:
            return self.module.get_global(name)
        
        signature = self.registered_functions.get(name)
        if signature is None:
            raise Exception(f'unknown function \'{name}\'')
        
        return lir.Function(self.module, signature, name)

@dataclass
class Scope:
    file: Path
    module: lir.Module
    builder: lir.IRBuilder
    parent: Optional['Scope'] = None
    children: list['Scope'] = field(default_factory=list)
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    type_map: TypeMap = field(default_factory=TypeMap)
    dependencies: list[Path] = field(default_factory=list)

    def __post_init__(self):
        if self.parent is not None:
            self.symbol_table = self.parent.symbol_table.clone()
            self.type_map = self.parent.type_map.clone()
            
            self.dependencies = self.parent.dependencies
            self.c_registry = self.parent.c_registry
        else:
            self.c_registry = CRegistry(self.module)

            info('Initializing global scope types')

            ref_type = self.module.context.get_identified_type('Ref')
            if ref_type.is_opaque:
                ref_type.set_body(lir.PointerType(lir.IntType(8)), lir.IntType(64))

            string_type = self.module.context.get_identified_type('string')
            if string_type.is_opaque:
                string_type.set_body(
                    lir.PointerType(lir.IntType(8)), lir.IntType(64), lir.PointerType(ref_type)
                )
            
            # primitive types
            self.type_map.add('int', lir.IntType(32))
            self.type_map.add('float', lir.FloatType())
            self.type_map.add('bool', lir.IntType(1))
            self.type_map.add('nil', lir.VoidType())
            
            # class types
            self.type_map.add('string', string_type)
            self.type_map.add('Ref', ref_type)

            self.type_map.add('__i8*', lir.PointerType(lir.IntType(8)))
            self.type_map.add('__i64', lir.IntType(64))
            
            self.type_map.add('any', lir.PointerType(lir.IntType(8)))
            self.type_map.add('function', lir.PointerType(lir.IntType(8)))

            info('Global scope types initialized')

    def make_child(self) -> 'Scope':
        child = Scope(self.file, self.module, self.builder, self)
        self.children.append(child)
        return child
    
    def merge(self, other: 'Scope'):
        self.symbol_table.merge(other.symbol_table)
        self.type_map.merge(other.type_map)
        self.dependencies.extend(other.dependencies)


def builtin(
    self,
    ret_type: Optional['Type'] = None, params: Optional[list['Param']] = None,
    generic_params: Optional[list[str]] = None, override_name: Optional[str] = None,
    is_property: bool = False
):
    """Decorator for registering a built-in function, method or property.

    Args:
        ret_type (Optional[Type], optional): The return type of the function in Cure IR.
        Defaults to None.
        params (Optional[list[Param]], optional): The parameters of the function in Cure IR.
        Defaults to None.
        generic_params (Optional[list[str]], optional): The generic parameters of the function. To use
        these in the return type or parameter types, use `GenericType.from_name()`. Defaults to None.
        override_name (Optional[str], optional): The name of the function defaults to the python
        name of the function, how it was defined. Use this override that if the name should be
        different or the function name is taken by a python function, e.g. print or assert.
        Defaults to None.
        is_property (bool, optional): Whether the function is a property. Functions that are a member
        of a `Class` object are considered methods, this overrides that. Defaults to False.
    """

    if ret_type is None:
        ret_type = self.scope.type_map.get('nil')
    
    if params is None:
        params = []
    
    if generic_params is None:
        generic_params = []
    
    def decorator(func):
        name = override_name or func.__name__
        is_class = isinstance(self, Class)
        if is_class:
            name = f'{self.type}.{name}'

        func.ret_type = ret_type
        func.params = params
        func.self = self

        flags = FunctionFlags(property=is_property and is_class, method=not is_property and is_class)
        cure_fn = Function(
            Position.zero(), ret_type, name, params, func, flags=flags, generic_params=generic_params
        )

        self.attrs[name] = cure_fn
        self.scope.symbol_table.add(Symbol(name, self.scope.type_map.get('function'), cure_fn))
        info(f'Built-in function {name}')
        return func
    
    return decorator


@dataclass
class CodegenArg:
    type: 'Type'
    value: lir.Value

@dataclass
class DefinitionContext:
    pos: Position
    scope: Scope
    args: list[CodegenArg]
    func: 'Function'

    def __post_init__(self):
        self.c_registry = self.scope.c_registry
        self.builder = self.scope.builder
        self.module = self.scope.module

        self.params = self.func.params
        self.ret_type = self.func.ret_type
    
    def arg(self, index_or_name: Union[int, str]):
        if isinstance(index_or_name, int):
            name = self.params[index_or_name].name
        else:
            name = index_or_name

        symbol = self.scope.symbol_table.get(name)
        if symbol is None:
            self.pos.comptime_error(self.scope, f'unknown parameter \'{name}\'')
        
        param = symbol.value
        if isinstance(symbol.type, lir.PointerType):
            param = self.builder.load(param)
        
        return CodegenArg(symbol.type, param)
    
    def arg_value(self, index_or_name: Union[int, str]):
        return self.arg(index_or_name).value
    
    def arg_type(self, index_or_name: Union[int, str]):
        return self.arg(index_or_name).type

    def arg_range(self, start: int, end: int):
        return self.args[start:end]
    
    def call(self, callee: str, args: list[CodegenArg], name: str = ''):
        return run_function(self.scope, callee, args, name)


class Lib:
    def __init__(self, scope: Scope):
        self.attrs: dict[str, Function] = {}
        self.scope = scope

        self.name = self.__class__.__name__

    def init(self):
        pass

    def add(self, lib_type: type[Union['Lib', 'Class']], *args, **kwargs):
        cls = lib_type(self.scope, *args, **kwargs)
        cls.init()

        for name, func in cls.attrs.items():
            self.attrs[name] = func
            info(f'Added function \'{name}\' from {lib_type.__name__}')

        return cls

class Class:
    def __init__(self, scope: Scope):
        self.attrs: dict[str, Function] = {}
        self.scope = scope

        self.name = self.__class__.__name__
        self.type = self.scope.type_map.get(self.name)
        if self.type is None:
            self.type = self.get_type()
            if self.type is None:
                raise RuntimeError(f'Class \'{self.name}\' has no type, override get_type()')
            
            self.scope.type_map.add(self.name, self.type)
    
    @staticmethod
    def get_type():
        ...
    
    def init(self):
        pass


@dataclass(**node_kwargs)
class Node(ABC):
    pos: Position
    type: 'Type'
                 
    @abstractmethod
    def codegen(self, scope: Scope):
        raise NotImplementedError
    
    def analyse(self, scope: Scope) -> 'Node':
        return self

@dataclass(**node_kwargs)
class Type(Node):
    type: lir.Type # type: ignore
    display: str
    
    def __str__(self) -> str:
        return self.display
    
    def codegen(self, _):
        return self.type

    def analyse(self, scope):
        typ = scope.type_map.get(self.display)
        if typ is None:
            self.pos.comptime_error(scope, f'unknown type \'{self.display}\'')
        
        info(f'Valid type \'{self.display}\'')
        return typ
    
    def as_pointer(self):
        return PointerType.from_type(self)

@dataclass(**node_kwargs)
class PointerType(Type):
    pointee: Type

    @staticmethod
    def from_type(pointee: Type):
        return PointerType(pointee.pos, lir.PointerType(pointee.type), pointee.display + '*', pointee)

    def __str__(self):
        return f'{str(self.pointee)}*'
    
    def codegen(self, _):
        return lir.PointerType(self.pointee.type)
    
    def analyse(self, scope):
        return PointerType(
            self.pos, self.type, self.display, self.pointee.analyse(scope)
        )

@dataclass(**node_kwargs)
class GenericType(Type):
    type: str # type: ignore
    
    def __str__(self):
        return self.type

    def codegen(self, _):
        return self.type

    @staticmethod
    def from_name(name: str):
        return GenericType(Position.zero(), name, name)

@dataclass(**node_kwargs)
class Program(Node):
    nodes: list[Node] = field(default_factory=list)
    
    def codegen(self, scope):
        for node in self.nodes:
            node.codegen(scope)
        
        return str(scope.module)
    
    def analyse(self, scope):
        return Program(self.pos, self.type.analyse(scope), [
            node.analyse(scope) for node in self.nodes
        ])

@dataclass(**node_kwargs)
class Param(Node):
    name: str
    is_mutable: bool = False
    
    def codegen(self, _):
        return self.type.type
    
    def analyse(self, scope):
        return Param(self.pos, self.type.analyse(scope), self.name, self.is_mutable)

@dataclass(**node_kwargs)
class Body(Node):
    nodes: list[Node] = field(default_factory=list)

    def decrement_references(self, scope: Scope):
        for symbol in scope.symbol_table.local_symbols.values():
            code_type = symbol.type.type
            if not isinstance(code_type, (lir.IdentifiedStructType, lir.LiteralStructType)):
                continue

            ref_type = scope.type_map.get('Ref')
            ref_index = index_of_type(code_type, lir.PointerType(ref_type.type))
            if ref_index == -1:
                continue

            run_function(scope, 'Ref.dec', [CodegenArg(ref_type, get_struct_field_value(
                scope.builder, symbol.value, ref_index, f'{symbol.name}_ref'
            ))])
    
    def codegen(self, scope):
        for node in self.nodes:
            if isinstance(node, Return):
                cleanup_block = scope.builder.append_basic_block('cleanup')
                scope.builder.branch(cleanup_block)
                scope.builder.position_at_end(cleanup_block)

                self.decrement_references(scope)

                return_block = scope.builder.append_basic_block('return')
                scope.builder.branch(return_block)
                scope.builder.position_at_end(return_block)

            node.codegen(scope)
    
    def analyse(self, scope):
        return Body(self.pos, self.type.analyse(scope), [
            node.analyse(scope) for node in self.nodes
        ])

@dataclass(**node_kwargs)
class Return(Node):
    value: Node
    
    def codegen(self, scope):
        value = self.value.codegen(scope)
        scope.builder.ret(value)
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        return Return(self.pos, value.type, value)

@dataclass(kw_only=True, **node_kwargs)
class FunctionFlags:
    static: bool = False
    property: bool = False
    method: bool = False

@dataclass(**node_kwargs)
class Function(Node):
    name: str
    params: list[Param] = field(default_factory=list)
    body: Body | Callable | None = field(default=None)
    overloads: list['Function'] = field(default_factory=list)
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    generic_params: list[str] = field(default_factory=list)
    
    @property
    def ret_type(self):
        return self.type

    def handle_generic(self, typ: 'Type', generic_map: dict[str, 'Type']):
        if isinstance(typ, GenericType):
            return generic_map[typ.type]
        else:
            return typ
    
    def codegen(self, scope: Scope, args: Optional[list[CodegenArg]] = None):
        if len(self.generic_params) > 0 and args is None:
            return self
        
        info(f'Compiling function \'{self.name}\'')
        
        generic_map = {}
        name = self.name
        if args is not None:
            info('Resolving generics')
            for arg, param in zip(args, self.params):
                if isinstance(param.type, GenericType):
                    generic_map[param.type.type] = arg.type.analyse(scope)
            
            generics_str = ', '.join(map(str, generic_map.values()))
            name = f'{self.name}<{generics_str}>'
            info(f'Generic function name {name}')
            info(f'Generic map: {generic_map}')
        
        if name in scope.module.globals:
            info('Function already defined')
            return scope.module.get_global(name)

        ret_type = self.handle_generic(self.ret_type, generic_map).type
        
        param_types = []
        for param in self.params:
            param_types.append(self.handle_generic(param.type, generic_map).type)
        
        func = lir.Function(scope.module, lir.FunctionType(ret_type, param_types), name)
        
        info('Created')
        scope.symbol_table.add(Symbol(func.name, scope.type_map.get('function'), func))
        info('Added to symbol table')
        if self.body is not None:
            body_scope = scope.make_child()
            body_block = func.append_basic_block('entry')
            body_scope.builder = lir.IRBuilder(body_block)

            if len(self.params) > 0:
                info('Allocating parameters')
                for i, param in enumerate(self.params):
                    if param.is_mutable:
                        param_value = body_scope.builder.alloca(param.type.type, name=param.name)
                        body_scope.builder.store(func.args[i], param_value)
                    else:
                        param_value = func.args[i]

                    body_scope.symbol_table.add(Symbol(
                        param.name, self.handle_generic(param.type, generic_map), param_value,
                        param.is_mutable
                    ))
            
            info('Building body')
            if isinstance(self.body, Body):
                info('Running codegen on body')
                self.body.codegen(body_scope)
                if self.ret_type == body_scope.type_map.get('nil'):
                    body_scope.builder.ret_void()
            elif callable(self.body):
                info('Calling body')
                ctx = DefinitionContext(self.pos, body_scope, args or [], self)
                res = self.body(ctx)
                if res is None:
                    body_scope.builder.ret_void()
                else:
                    body_scope.builder.ret(res)
        
        info('Done')
        return func
    
    def analyse(self, scope):
        info(f'Analyzing function \'{self.name}\'')
        name = self.name
        if len(self.generic_params) > 0:
            generic_params_str = ', '.join(self.generic_params)
            name = f'{self.name}<{generic_params_str}>'

        func = Function(
            self.pos, self.type.analyse(scope), name,
            [param.analyse(scope) for param in self.params],
            self.body, [overload.analyse(scope) for overload in self.overloads],
            self.generic_params
        )

        scope.symbol_table.add(Symbol(name, scope.type_map.get('function'), func))
        info('Added to symbol table')
        
        body = self.body
        if body is not None:
            body_scope = scope.make_child()
            for param in self.params:
                body_scope.symbol_table.add(Symbol(param.name, param.type, param, param.is_mutable))

            body = self.body.analyse(body_scope)
            info('Analysed body')
        
        info('Done')
        return Function(
            func.pos, func.type, func.name, func.params, body, func.overloads, func.flags,
            func.generic_params
        )

@dataclass(**node_kwargs)
class Variable(Node):
    name: str
    value: Node
    is_mutable: bool = False
    op: Optional[str] = None
    
    def codegen(self, scope):
        info(f'Compiling variable \'{self.name}\'')
        info('Allocating pointer')
        ptr = scope.builder.alloca(self.type.type, name=self.name)
        scope.builder.store(self.value.codegen(scope), ptr)

        scope.symbol_table.add(Symbol(self.name, self.type, ptr, self.is_mutable))
        info('Added to symbol table')
        info('Done')
        return ptr
    
    def analyse(self, scope):
        info(f'Analyzing variable \'{self.name}\'')
        value = self.value.analyse(scope)

        info('Analysed value')
        if scope.symbol_table.has(self.name):
            info('Variable already defined, performing assignment')
            return Assignment(self.pos, value.type, self.name, value, self.op).analyse(scope)
        
        scope.symbol_table.add(Symbol(self.name, value.type, value, self.is_mutable))
        info('Added to symbol table')
        info('Done')
        return Variable(self.pos, value.type, self.name, value, self.is_mutable)

@dataclass(**node_kwargs)
class Assignment(Node):
    name: str
    value: Node
    op: Optional[str] = None
    
    def codegen(self, scope):
        info(f'Compiling assignment \'{self.name}\'')
        info('Getting pointer')
        symbol = scope.symbol_table.get(self.name)
        ptr = symbol.value

        info('Storing value in pointer')
        scope.builder.store(self.value.codegen(scope), ptr)
    
    def analyse(self, scope):
        info(f'Analyzing assignment \'{self.name}\'')
        symbol = scope.symbol_table.get(self.name)
        if not symbol.is_mutable:
            self.pos.comptime_error(scope, f'\'{self.name}\' is immutable')
        
        info('Done')
        return self

@dataclass(**node_kwargs)
class Elseif(Node):
    cond: Node
    body: Body
    
    def codegen(self, _):
        raise NotImplementedError

@dataclass(**node_kwargs)
class If(Node):
    cond: Node
    body: Body
    else_body: Optional[Body] = field(default=None)
    elseifs: list[Elseif] = field(default_factory=list)
    
    def codegen(self, _):
        raise NotImplementedError

@dataclass(**node_kwargs)
class While(Node):
    cond: Node
    body: Body
    
    def codegen(self, _):
        raise NotImplementedError

@dataclass(**node_kwargs)
class Break(Node):
    def codegen(self, _):
        raise NotImplementedError

@dataclass(**node_kwargs)
class Continue(Node):
    def codegen(self, _):
        raise NotImplementedError

@dataclass(**node_kwargs)
class Use(Node):
    path: str
    
    def codegen(self, scope):
        file = Path(self.path).resolve()
        if file.exists():
            raise NotImplementedError('local use')
        else:
            file = STDLIB_PATH / self.path
            if not file.exists():
                self.pos.comptime_error(scope, f'unknown library \'{self.path}\'')
            
            if not file.is_dir():
                self.pos.comptime_error(scope, f'use path \'{self.path}\' is not a directory')

            file_module = lir.Module(file.name)
            file_module.triple = binding.get_default_triple()
            file_scope = Scope(file, file_module, lir.IRBuilder())

            lib_name = file.name
            module = import_module(f'cure.stdlib.{lib_name}.{lib_name}')
            lib = getattr(module, lib_name)(file_scope)
            lib.init()

            for k, v in lib.attrs.items():
                ir_func = v.codegen(file_scope)
                file_scope.symbol_table.add(Symbol(k, file_scope.type_map.get('function'), ir_func))
                if isinstance(ir_func, Function): # generic function
                    continue

                extern_func = lir.Function(scope.module, ir_func.function_type, k)
                extern_func.linkage = 'external'
            
            ll_file = file.with_suffix('.ll')
            ll_file.write_text(str(file_module))

            obj_file = file.with_suffix('.o')
            run(f'clang -c {ll_file} -o {obj_file}', shell=True)

            scope.dependencies.append(file)

        return self

    def analyse(self, scope):
        file = Path(self.path).resolve()
        if file.exists():
            raise NotImplementedError('local use')
        else:
            file = STDLIB_PATH / self.path
            if not file.exists():
                self.pos.comptime_error(scope, f'unknown library \'{self.path}\'')
            
            if not file.is_dir():
                self.pos.comptime_error(scope, f'use path \'{self.path}\' is not a directory')
            
            lib_name = file.name
            module = import_module(f'cure.stdlib.{lib_name}.{lib_name}')
            lib = getattr(module, lib_name)(scope)
            lib.init()

        return self

@dataclass(**node_kwargs)
class Int(Node):
    value: int
    
    def codegen(self, _):
        return lir.Constant(self.type.type, self.value)
    
    def analyse(self, scope):
        return Int(self.pos, self.type.analyse(scope), self.value)

@dataclass(**node_kwargs)
class Float(Node):
    value: float
    
    def codegen(self, _):
        return lir.Constant(self.type.type, self.value)
    
    def analyse(self, scope):
        return Float(self.pos, self.type.analyse(scope), self.value)

@dataclass(**node_kwargs)
class String(Node):
    value: str
    
    def codegen(self, scope):
        ptr = create_string_constant(scope.module, self.value, scope.module.get_unique_name('str'))
        length = lir.Constant(scope.type_map.get('__i64').type, len(self.value))
        return run_function(scope, 'string.new', [
            CodegenArg(scope.type_map.get('__i8*'), ptr),
            CodegenArg(scope.type_map.get('__i64'), length)
        ])

@dataclass(**node_kwargs)
class Bool(Node):
    value: bool
    
    def codegen(self, _):
        return lir.Constant(self.type.type, self.value)
    
    
    def analyse(self, scope):
        return Bool(self.pos, self.type.analyse(scope), self.value)

@dataclass(**node_kwargs)
class Id(Node):
    name: str
    
    def codegen(self, scope):
        symbol = scope.symbol_table.get(self.name)
        value = symbol.value
        if isinstance(value.type, lir.PointerType):
            return scope.builder.load(value)
        
        return value
    
    def analyse(self, scope):
        symbol = scope.symbol_table.get(self.name)
        if symbol is None:
            self.pos.comptime_error(scope, f'unknown name \'{self.name}\'')
        
        return Id(self.pos, symbol.type, symbol.name)

@dataclass(**node_kwargs)
class Call(Node):
    callee: Id
    args: list[Node] = field(default_factory=list)
    
    def codegen(self, scope):
        return run_function(scope, self.callee.name, [
            CodegenArg(arg.type, arg.codegen(scope)) for arg in self.args
        ])
    
    def analyse(self, scope):
        callee = self.callee.analyse(scope)
        callee_name = self.callee.name
        symbol = scope.symbol_table.get(callee_name)
        fn = symbol.value
        if not isinstance(fn, Function):
            self.pos.comptime_error(scope, f'\'{callee_name}\' is not a function')
        
        args = [arg.analyse(scope) for arg in self.args]
        return Call(self.pos, fn.ret_type, callee, args)

@dataclass(**node_kwargs)
class Cast(Node):
    value: Node
    
    def codegen(self, _):
        raise NotImplementedError

@dataclass(**node_kwargs)
class New(Node):
    new_type: Type
    args: list[Node] = field(default_factory=list)
    
    def codegen(self, _):
        raise NotImplementedError

@dataclass(**node_kwargs)
class Operation(Node):
    op: str
    left: Node
    right: Node | None
    
    def codegen(self, _):
        raise NotImplementedError
    
    def analyse(self, scope):
        op_name = op_map[self.op]
        left = self.left.analyse(scope)
        right = self.right.analyse(scope) if self.right is not None else None
        if right is None:
            args = [left]
            call_name = f'{left.type}.{op_name}'
            err_msg = f'invalid operation \'{self.op}\' on type \'{left.type}\''
        else:
            args = [left, right]
            call_name = f'{left.type}.{op_name}.{right.type}'
            err_msg = f'invalid operation \'{self.op}\' on types \'{left.type}\' and \'{right.type}\''
        
        symbol = scope.symbol_table.get(call_name)
        if symbol is None:
            self.pos.comptime_error(scope, err_msg)
        
        return Call(
            self.pos, scope.type_map.get('any'), Id(self.pos, symbol.type, symbol.name), args
        ).analyse(scope)

@dataclass(**node_kwargs)
class Attribute(Node):
    value: Node
    attr: str
    args: Optional[list[Node]] = None
    
    def codegen(self, _):
        raise NotImplementedError

@dataclass(**node_kwargs)
class Ternary(Node):
    cond: Node
    true: Node
    false: Node
    
    def codegen(self, scope):
        return scope.builder.select(
            self.cond.codegen(scope), self.true.codegen(scope), self.false.codegen(scope)
        )
    
    def analyse(self, scope):
        cond = self.cond.analyse(scope)
        if cond.type != scope.type_map.get('bool'):
            self.pos.comptime_error(scope, 'condition must be a boolean')
        
        true = self.true.analyse(scope)
        false = self.false.analyse(scope)
        if true.type != false.type:
            self.pos.comptime_error(scope, 'true and false must have the same type')
        
        return Ternary(self.pos, true.type, cond, true, false)

@dataclass(**node_kwargs)
class Bracketed(Node):
    value: Node
    
    def codegen(self, scope):
        return self.value.codegen(scope)
    
    def analyse(self, scope):
        value = self.value.analyse(scope)
        return Bracketed(self.pos, value.type, value)
