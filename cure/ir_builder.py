from antlr4.error.ErrorListener import ErrorListener as ANTLRErrorListener
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken

from cure.parser.CureVisitor import CureVisitor
from cure.parser.CureParser import CureParser
from cure.parser.CureLexer import CureLexer
from cure.ir import (
    Program, Scope, Position, Function, Param, Int, Float, String, Bool, Id, Return, Body, Call,
    Cast, Operation, New, Use, If, While, Variable, Ternary, Bracketed, Attribute, Break, Continue,
    FunctionFlags, Elseif, Type
)


class ErrorListener(ANTLRErrorListener):
    def __init__(self, scope: Scope):
        self.scope = scope
    
    def syntaxError(self, _, offendingSymbol: CommonToken, line: int, column: int, _msg, _e):
        pos = Position(line, column)
        pos.comptime_error(self.scope, f'invalid syntax \'{offendingSymbol.text}\'')

class IRBuilder(CureVisitor):
    def __init__(self, scope: Scope):
        self.scope = scope
    
    def pos(self, ctx):
        if hasattr(ctx, 'start'):
            return Position(ctx.start.line, ctx.start.column)
        elif hasattr(ctx, 'line') and hasattr(ctx, 'column'):
            return Position(ctx.line, ctx.column)
        else:
            return Position.zero()
    
    def build(self):
        lexer = CureLexer(InputStream(self.scope.file.read_text()))
        parser = CureParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(ErrorListener(self.scope))
        return self.visitProgram(parser.program())
    
    def visitProgram(self, ctx):
        return Program(
            self.pos(ctx), self.scope.type_map.get('any'), [self.visit(stmt) for stmt in ctx.stmt()]
        )
    
    def visitType(self, ctx):
        return Type(self.pos(ctx), None, ctx.getText())
    
    def visitArgs(self, ctx):
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitArg(self, ctx):
        return self.visit(ctx.expr())
    
    def visitReturn(self, ctx):
        expr = self.visit(ctx.expr())
        return Return(self.pos(ctx), expr.type, expr)
    
    def visitBreak(self, ctx):
        return Break(self.pos(ctx), self.scope.type_map.get('any'))
    
    def visitContinue(self, ctx):
        return Continue(self.pos(ctx), self.scope.type_map.get('any'))
    
    def visitBody(self, ctx):
        return Body(
            self.pos(ctx), self.scope.type_map.get('any'),
            [self.visit(stmt) for stmt in ctx.bodyStmts()]
        )
    
    def visitParams(self, ctx):
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitParam(self, ctx):
        return Param(
            self.pos(ctx), self.visitType(ctx.type_()), ctx.ID().getText(),
            ctx.MUTABLE() is not None
        )
    
    def visitFuncAssign(self, ctx):
        return Function(
            self.pos(ctx), self.visitType(ctx.return_type) if ctx.return_type is not None else
                self.scope.type_map.get('nil'), ctx.ID().getText(),
            self.visitParams(ctx.params()), self.visitBody(ctx.body()),
            flags=FunctionFlags()
        )
    
    def visitVarAssign(self, ctx):
        return Variable(
            self.pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText(), self.visit(ctx.expr()),
            ctx.MUTABLE() is not None, ctx.op.text if ctx.op is not None else None
        )
    
    def visitIfStmt(self, ctx):
        return If(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()),
            self.visitBody(ctx.body()), self.visitElseStmt(ctx.elseStmt()),
            [self.visitElseifStmt(elseif) for elseif in ctx.elseifStmt()]
        )
    
    def visitElseStmt(self, ctx):
        return self.visitBody(ctx.body()) if ctx is not None else None
    
    def visitElseifStmt(self, ctx):
        return Elseif(
            self.pos(ctx), self.scope.type_map.get('any'),
            self.visit(ctx.expr()), self.visitBody(ctx.body())
        )
    
    def visitWhileStmt(self, ctx):
        return While(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()),
            self.visitBody(ctx.body())
        )
    
    def visitUseStmt(self, ctx):
        return Use(self.pos(ctx), self.scope.type_map.get('any'), ctx.STRING().getText()[1:-1])
    
    def visitInt(self, ctx):
        return Int(self.pos(ctx), self.scope.type_map.get('int'), int(ctx.getText()))
    
    def visitFloat(self, ctx):
        return Float(self.pos(ctx), self.scope.type_map.get('float'), float(ctx.getText()))
    
    def visitString(self, ctx):
        return String(self.pos(ctx), self.scope.type_map.get('string'), ctx.getText()[1:-1])
    
    def visitBool(self, ctx):
        return Bool(self.pos(ctx), self.scope.type_map.get('bool'), ctx.getText() == 'true')
    
    def visitId(self, ctx):
        return Id(self.pos(ctx), self.scope.type_map.get('any'), ctx.getText())
    
    def visitCall(self, ctx):
        return Call(
            self.pos(ctx), self.scope.type_map.get('any'),
            Id(self.pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText()),
            self.visitArgs(ctx.args())
        )
    
    def visitParen(self, ctx):
        expr = self.visit(ctx.expr())
        return Bracketed(self.pos(ctx), expr.type, expr)
    
    def visitCast(self, ctx):
        return Cast(self.pos(ctx), self.visitType(ctx.type_()), self.visit(ctx.expr()))
    
    def visitAttr(self, ctx):
        return Attribute(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()), ctx.ID().getText(),
            self.visitArgs(ctx.args()) if ctx.LPAREN() is not None else None
        )
    
    def visitTernary(self, ctx):
        return Ternary(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr(1)),
            self.visit(ctx.expr(0)), self.visit(ctx.expr(2))
        )
    
    def visitNew(self, ctx):
        return New(
            self.pos(ctx), self.scope.type_map.get('any'), self.visitType(ctx.type_()),
            self.visitArgs(ctx.args())
        )
    
    def visitOperation(self, ctx):
        pos = self.pos(ctx)
        op = ctx.op.text
        if isinstance(ctx.expr(), list):
            left, right = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        else:
            left, right = self.visit(ctx.expr()), None
        
        return Operation(pos, self.scope.type_map.get('any'), op, left, right)
    
    def visitAddition(self, ctx):
        return self.visitOperation(ctx)
    
    def visitMultiplication(self, ctx):
        return self.visitOperation(ctx)
    
    def visitRelational(self, ctx):
        return self.visitOperation(ctx)
    
    def visitLogical(self, ctx):
        return self.visitOperation(ctx)
    
    def visitUnary(self, ctx):
        return self.visitOperation(ctx)
