# CureLLVM
 The Cure programming language

Cure is a programming language that uses LLVM to achieve incredibly fast programs with the simplicity of a language similar to Python and C#.

### Features
Note that Cure is still an extremely new programming language, so this does not include all or upcoming features.

- `print`, `input` (with string overload) and `error` functions.
- variables (defaults to immutable)
- functions
- `int`, `float`, `string`, `bool` and `nil` types.
- type attributes
- arithmetic and logical operations

### How to run
1. Install Python with the pip package manager and run `pip install -r requirements.txt`
2. Install LLVM
3. Clone this repository
    - You can use `git` or download as a zip then unzip
4. Run the repository
    - Type in `python main.py build <file>` replace `<file>` with your `.cure` file you want to build to a .exe file
