# CureLLVM
A programming language using llvmlite

Cure is a programming language that is designed to be very easy-to-learn, fast, general purpose and safe. The language compiles to LLVM offering high performance.

---

## Features
- **Speed**: Due to Cure being compiled using LLVM, it is very fast at runtime. It is also quite fast to compile.
- **Simplicity**: Cure is designed to be simple to use and learn.
- **Static typing**: Cure is statically typed meaning that the compiler will check for errors at compile time. Cure also has type inference on variables, so you don't need to define the types of variables. You do need to define the types on parameters and what functions return though.

---

## Running the language
1. Clone the repository
    - If you have the `git` command line tool, you can use that to install the repository using: `git clone https://github.com/LemurGamingYT1/Cure.git`
    - If you don't have `git`, then you can install the repository as a .zip by clicking the drop down menu: 'Code' and then 'Download ZIP'
2. Install Python
    - Install Python 3.12.0 or higher: https://www.python.org/downloads/
    - During the setup, add Python to PATH and install pip and run the command: `pip install -r requirements.txt` in the directory you have downloaded this repository.
3. Install LLVM from https://github.com/llvm/llvm-project/releases
4. Run the compiler
    - Add the 'bin' directory of the compiler to your PATH environment variable
    - Run the compiler using the command: `cure [actions] [options]`
    - Use `cure -h` to see all available options
