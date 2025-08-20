# Compiler Design
 How the compiler is works internally from source to exe.

### 1. Scope
First, the source is obtained from reading the input files when using the `build` command and after that, the file is passed into creating the global scope. The scope is a python class that holds important things that a scope has including: it's parent, defined symbols and types, dependencies, etc.

### 2. Types
Now it's time for the types to be initialised. The types are defined using a display type (i.e. what is displayed in, for example, error messages) and an LLVM type (for code generation). Some types may need a struct type instead of just one type. The `Ref` object is one of them and is invisible to the programmer as it's handled internally for memory management. The `string` is another one that uses a struct as it uses a `u8*` as the data and an `i32` for the length.

### 3. Built-ins
Now that the types are initialised, we can start initialising the libraries that Cure uses. The one included in every scope is the `builtins` library. The python module at `cure.stdlib.builtins.builtins` is loaded dynamically using `importlib.import_module`. It loads the `builtins` python class inside that module which initialises the `Ref`, `int`, `float`, `string`, `bool` and `Math` classes, along with some built-in functions such as `print`.

### 4. The Built-in Function compilation
This is a big step.

Built-in functions are functions that the compiler recognises and compiles, they're not defined by the programmer but they can be used by the programmer. All built-in functions are defined in python and use `llvmlite`. When registering a built-in function, multiple steps occur:
1. In the python classes, a special decorator is used to define the return type, parameters and function flags of the function. The decorator adds these attributes to the python function.
2. The python function takes in a `DefinitionContext` which provides an interface to the parameters.
3. The function is added to the scope's `SymbolTable`.
4. When the function is called, a new LLVM IR function (`llvmlite.ir.Function`) is defined if it doesn't exist, if it does exist, then the function is called through the `llvmlite.ir.IRBuilder.call` method.
5. If the function doesn't exist, the definition logic takes place.
6. The function scope is set up, parameters are allocated and the python function is called using a newly created `DefinitionContext`.
7. After the python function returns, the function is called.

TODO
