from typing import Any

from llvmlite import ir


def NULL(type: ir.Type | None = None):
    """Returns the NULL value of the type"""
    if type is None:
        type = ir.PointerType(ir.IntType(8)) # void*
    
    if not isinstance(type, ir.PointerType):
        type = ir.PointerType(type)
    
    return ir.Constant(type, None)

def NULL_BYTE():
    """Returns a null-terminator (\\0)"""
    return ir.Constant(ir.IntType(8), None) # \0

def zero(int_width: int):
    """Returns an integer constant with the given width with a value of 0"""
    return ir.Constant(ir.IntType(int_width), 0)

def float_zero():
    """Returns a float constant with the value 0.0"""
    return ir.Constant(ir.FloatType(), 0.0)

def get_type_size(builder: ir.IRBuilder, llvm_type: ir.Type, name: str = ''):
    """Get the size of a type, this done at runtime so it cannot be used as a constant"""
    # Create a null pointer of the type
    null_ptr = ir.Constant(ir.PointerType(llvm_type), None)
    
    # GEP to the next element (index 1)
    size_ptr = builder.gep(null_ptr, [ir.Constant(ir.IntType(32), 1)], True)
    
    # Convert pointer to integer to get the size
    size = builder.ptrtoint(size_ptr, ir.IntType(64), name)
    
    return size

def index_of_type(type: ir.LiteralStructType | ir.IdentifiedStructType, elem_type: ir.Type):
    """Find the index of a type in a LiteralStructType or IdentifiedStructType (returns -1 if the type is not found)"""
    try:
        return type.elements.index(elem_type)
    except ValueError:
        return -1

def cast_value(builder: ir.IRBuilder, value: ir.Value, type: ir.Type, name: str = ''):
    """Converts the value to the type in any possible way"""
    value_type = value.type
    if isinstance(type, ir.IntType) and isinstance(value_type, ir.IntType):
        if type.width > value_type.width:
            return builder.zext(value, type, name)
        elif type.width < value_type.width:
            return builder.trunc(value, type, name)
        else:
            # type.width == value_type.width
            return value
    elif isinstance(type, ir.FloatType) and isinstance(value_type, ir.IntType):
        return builder.sitofp(value, type, name)
    elif isinstance(type, ir.IntType) and isinstance(value_type, ir.FloatType):
        return builder.fptosi(value, type, name)
    elif isinstance(type, ir.DoubleType) and isinstance(value_type, ir.FloatType):
        return builder.fpext(value, type, name)
    elif isinstance(type, ir.FloatType) and isinstance(value_type, ir.DoubleType):
        return builder.fptrunc(value, type, name)
    elif isinstance(type, ir.IntType) and isinstance(value_type, ir.PointerType):
        return builder.ptrtoint(value, type, name)
    elif isinstance(type, ir.PointerType) and isinstance(value_type, ir.IntType):
        return builder.inttoptr(value, type, name)
    else:
        return builder.bitcast(value, type, name)

def get_or_add_global(module: ir.Module, name: str, global_value: Any, **kwargs):
    """Gets or adds a global value"""
    if name in module.globals:
        return module.get_global(name)
    
    module.add_global(global_value)
    for k, v in kwargs.items():
        setattr(global_value, k, v)
    
    return global_value


def max_value(bits: int):
    """Returns the maximum value for the given number of bits"""
    assert bits > 0
    return 2 ** (bits - 1) - 1

def min_value(bits: int):
    """Returns the minimum value for the given number of bits"""
    assert bits > 0
    return -2 ** (bits - 1)


def create_struct_value(builder: ir.IRBuilder, struct_type: ir.Type, field_values: list[ir.Value]):
    """Create a struct value from field values"""
    struct_val = ir.Constant(struct_type, ir.Undefined)
    for i, field_val in enumerate(field_values):
        struct_val = builder.insert_value(struct_val, field_val, i)
    
    return struct_val

def allocate_struct(builder: ir.IRBuilder, struct_type: ir.Type, name: str = ''):
    """Allocate space for a struct on the stack"""
    return builder.alloca(struct_type, name=name)

def get_struct_field_ptr(builder: ir.IRBuilder, struct: ir.Value, field_index: int, name: str = ''):
    """Get pointer to a struct field (struct must be allocated)"""
    field_idx = ir.Constant(ir.IntType(32), field_index)
    return builder.gep(struct, [zero(32), field_idx], True, name)

def get_struct_field_value(builder: ir.IRBuilder, struct: ir.Value, field_index: int, name: str = ''):
    """Get a field value from a struct value (the struct can be allocated or not allocated)"""
    if isinstance(struct.type, ir.PointerType):
        ptr = get_struct_field_ptr(builder, struct, field_index, f'{name}_ptr')
        return builder.load(ptr)
    
    return builder.extract_value(struct, field_index, name)

def set_struct_field(builder: ir.IRBuilder, struct: ir.Value, field_index: int, value: ir.Value,
                     name: str = ''):
    """Set a field in a struct (struct must be allocated)"""
    ptr = get_struct_field_ptr(builder, struct, field_index, name)
    builder.store(value, ptr)


def create_string_constant(module: ir.Module, text: str, name: str = ''):
    """Create a global string constant and return pointer to it"""
    if not text.endswith('\0'):
        text += '\0'
    
    const_type = ir.ArrayType(ir.IntType(8), len(text))
    const = ir.GlobalVariable(module, const_type, name or module.get_unique_name('str'))
    const.initializer = ir.Constant(const_type, bytearray(text.encode('utf-8')))
    const.global_constant = True
    const.linkage = 'internal'
    
    return ir.Constant.gep(const, [zero(32), zero(32)])


def create_buffer(builder: ir.IRBuilder, element_type: ir.Type, size: int, 
                 name: str = "") -> ir.Value:
    """Create a buffer (array) on the stack"""
    array_type = ir.ArrayType(element_type, size)
    return builder.alloca(array_type, name=name)

def create_buffer_ptr(builder: ir.IRBuilder, element_type: ir.Type, size: int, 
                     name: str = "") -> ir.Value:
    """Create a buffer and return pointer to first element"""
    buffer = create_buffer(builder, element_type, size, name)
    return builder.bitcast(buffer, ir.PointerType(element_type))

def get_buffer_element_ptr(builder: ir.IRBuilder, buffer_ptr: ir.Value, 
                          index: ir.Value) -> ir.Value:
    """Get pointer to buffer element at index"""
    return builder.gep(buffer_ptr, [index], True)

def set_buffer_element(builder: ir.IRBuilder, buffer_ptr: ir.Value, 
                      index: ir.Value, value: ir.Value) -> None:
    """Set buffer element at index"""
    element_ptr = get_buffer_element_ptr(builder, buffer_ptr, index)
    builder.store(value, element_ptr)

def get_buffer_element(builder: ir.IRBuilder, buffer_ptr: ir.Value, 
                      index: ir.Value) -> ir.Value:
    """Get buffer element at index"""
    element_ptr = get_buffer_element_ptr(builder, buffer_ptr, index)
    return builder.load(element_ptr)

def create_static_buffer(module: ir.Module, element_type: ir.Type, size: int, name = ''):
    buf_type = ir.ArrayType(element_type, size)
    buf = ir.GlobalVariable(module, buf_type, name or module.get_unique_name())
    buf.initializer = ir.Constant(buf_type, None)
    buf.linkage = 'internal'

    return ir.Constant.gep(buf, [zero(32), zero(32)])


def create_ternary(builder: ir.IRBuilder, condition: ir.Value, 
                  true_val: ir.Value, false_val: ir.Value) -> ir.Value:
    """Create ternary operator: condition ? true_val : false_val"""
    return builder.select(condition, true_val, false_val)


def create_while_loop(builder: ir.IRBuilder, condition_func, body_func):
    """Create a while loop"""
    
    function = builder.function
    
    # Create blocks
    condition_block = function.append_basic_block('while_condition')
    body_block = function.append_basic_block('while_body')
    exit_block = function.append_basic_block('while_exit')
    
    # Jump to condition block (only if current block isn't terminated)
    if not builder.block.is_terminated:
        builder.branch(condition_block)
    
    # Condition block
    builder.position_at_end(condition_block)
    condition = condition_func(builder)
    
    # Only add cbranch if the block isn't already terminated
    if not builder.block.is_terminated:
        builder.cbranch(condition, body_block, exit_block)
    
    # Body block
    builder.position_at_end(body_block)
    body_func(builder)
    
    # Loop back to condition (only if not terminated)
    if not builder.block.is_terminated:
        builder.branch(condition_block)
    
    # Exit block - position builder here for continuation
    builder.position_at_end(exit_block)
