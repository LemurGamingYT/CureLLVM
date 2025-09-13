from copy import copy
from abc import ABC

from cure.ir import Node, Program, Scope


class CompilerPass(ABC):
    def __init__(self, scope: Scope):
        self.scope = scope
    
    @classmethod
    def run(cls, scope: Scope, program: Program):
        self = cls(scope)
        return self.visit(program)
    
    def visit(self, node: Node):
        method_name = f'visit_{type(node).__name__}'
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(node)
        else:
            raise AttributeError(f'No method {method_name}')

    def visit_children(self, node: Node):
        new_node = copy(node)
        for child in new_node.children:
            child = self.visit(child)
        
        return new_node
