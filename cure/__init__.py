from dataclasses import dataclass
from sys import exit as sys_exit
from logging import debug, info
from subprocess import run
from pathlib import Path
from typing import cast

from cure.passes.code_generation import CodeGeneration
from cure.parser.ir_builder import CureIRBuilder
from cure.passes.analyser import Analyser
from cure import ir


HELP = """usage: cure [action] [options]

actions: build, help
"""

@dataclass
class CompileOptions:
    optimize: bool


def parse(scope: ir.Scope, _: CompileOptions):
    info(f'Compiling {scope.file.as_posix()}')
    program = CureIRBuilder(scope).build()

    info(f'Parsed {scope.file.as_posix()}')
    return program

def compile_to_str(scope: ir.Scope, options: CompileOptions):
    program = parse(scope, options)
    program = Analyser.run(scope, program)
    return CodeGeneration.run(scope, cast(ir.Program, program))

def compile_to_ll(scope: ir.Scope, options: CompileOptions):
    info(f'Compiling {scope.file.as_posix()} to an LLVM IR file (.ll)')
    code = compile_to_str(scope, options)
    debug(f'LLVM IR = {code}')
    ll_file = scope.file.with_suffix('.ll')
    ll_file.write_text(code)
    info(f'Wrote to {ll_file.as_posix()}')
    return ll_file

def compile_to_exe(scope: ir.Scope, options: CompileOptions):
    ll_file = compile_to_ll(scope, options)
    exe_file = scope.file.with_suffix(f'.{scope.target.exe_ext}')
    info(f'Compiling to executable file {exe_file.as_posix()} using clang')
    flags: list[str] = []
    if options.optimize:
        flags.append('-O2')
    
    flags_str = ' '.join(flags)
    run(f'clang {ll_file.absolute().as_posix()} -o {exe_file} {flags_str}')
    return exe_file


class CureArgParser:
    def __init__(self, args: list[str]):
        self.args = args

    def parse(self):
        if len(self.args) == 1:
            self.__help()
            return
        
        action = self.get(1)
        info(f'Found CLI action {action}')
        match action:
            case 'build':
                self.__build()
            case 'run':
                self.__run()
            case 'help':
                self.__help()
            case _:
                print(f"""{HELP}
invalid action {action}'""")
    
    def get(self, arg_index: int):
        if len(self.args) <= arg_index:
            return None
        
        return self.args[arg_index]
    
    def flag(self, name: str):
        try:
            i = self.args.index(f'--{name}')
            if len(self.args) - 1 >= i:
                return True
            
            next_value = self.args[i + 1]
            if next_value.startswith('-'):
                return True
            
            return next_value
        except ValueError:
            return None
    
    def __help(self):
        print(HELP)

    def __build(self):
        file_str = self.get(2)
        if file_str is None:
            print("""cure build [file]
file argument not given""")
            sys_exit(1)
        
        file = Path(file_str)
        if not file.exists():
            print("""cure build [file]
file does not exist""")
            sys_exit(1)
        
        if not file.is_file():
            print("""cure build [file]
file is not a file""")
            sys_exit(1)
        
        optimize = self.flag('optimize')
        options = CompileOptions(optimize)
        info(f'Building file {file.as_posix()} with options {options}')

        scope = ir.Scope(file)
        compile_to_exe(scope, options)
