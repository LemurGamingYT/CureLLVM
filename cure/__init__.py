from sys import exit as sys_exit, stderr
from logging import info, error
from subprocess import run
from pathlib import Path

from llvmlite import ir as lir, binding

from cure.ir import Scope, Use, Position
from cure.ir_builder import IRBuilder


def parse(scope: Scope):
    ir_builder = IRBuilder(scope)
    return ir_builder.build()

def compile_to_str(scope: Scope):
    program = parse(scope)
    program.nodes.insert(0, Use(Position.zero(), scope.type_map.get('any'), 'builtins'))
    program = program.analyse(scope)
    return program.codegen(scope)

def compile_to_exe(scope: Scope):
    code = compile_to_str(scope)

    ll_file = scope.file.with_suffix('.ll')
    ll_file.write_text(code)

    info(f'Compiled to LLVM IR {ll_file}')

    obj_files = []
    for dep in scope.dependencies:
        if not dep.is_dir():
            continue

        obj_files.append(str(dep.with_suffix('.o')))

    exe_file = scope.file.with_suffix('.exe')
    obj_files_str = ' '.join(obj_files)
    cmd = f'clang {ll_file} {obj_files_str} -o {exe_file}'
    info(f'Running {cmd}')
    res = run(cmd, shell=True)
    if res.returncode != 0:
        error(f'Failed to compile {scope.file} to an executable file')
        print(f'Errors occurred while trying to build {scope.file}', file=stderr)
        print(f'Return code: {res.returncode}', file=stderr)
        sys_exit(1)
    
    return exe_file

class ArgParser:
    def __init__(self, args: list[str]):
        self.args = args
    
    def parse(self):
        action = self.arg(0)
        info(f'CLI action: {action}')

        match action:
            case 'build':
                self.build()
            case _:
                print('Usage: cure <action> <file>')
                if action is None:
                    print('No action')
                else:
                    print(f'Unknown action \'{action}\'')
                
                sys_exit(1)

    def arg(self, index: int):
        if index < len(self.args):
            return self.args[index]
        
        return None
    
    def build(self, file_path: str | None = None):
        if file_path is None:
            file_path = self.arg(1)
        
        if file_path is None:
            print('Usage: cure build <file>')
            print('No file')
            sys_exit(1)
        
        path = Path(file_path).resolve()
        info(f'Building {path}')
        if not path.exists():
            print('Usage: cure build <file>')
            print(f'File \'{file_path}\' does not exist')
            sys_exit(1)
        
        if not path.is_file():
            print('Usage: cure build <file>')
            print(f'File \'{file_path}\' is not a file')
            sys_exit(1)
        
        module = lir.Module('main')
        module.triple = binding.get_default_triple()
        
        info(f'Compiling {path} to executable')
        scope = Scope(path, module, lir.IRBuilder())
        out = compile_to_exe(scope)
        info(f'Compiled {path} to executable at {out}')
