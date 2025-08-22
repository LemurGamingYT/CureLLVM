# Generated from cure/parser/Cure.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,46,213,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,1,0,5,0,36,8,0,10,0,12,0,39,9,0,1,
        0,1,0,1,1,1,1,1,1,1,1,1,1,5,1,48,8,1,10,1,12,1,51,9,1,1,2,1,2,1,
        2,1,2,1,2,3,2,58,8,2,1,3,1,3,1,3,1,3,1,3,3,3,65,8,3,1,4,1,4,5,4,
        69,8,4,10,4,12,4,72,9,4,1,4,1,4,1,5,1,5,1,5,1,5,5,5,80,8,5,10,5,
        12,5,83,9,5,1,5,3,5,86,8,5,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,
        8,1,8,1,8,1,9,1,9,1,9,1,9,3,9,104,8,9,1,9,1,9,1,9,3,9,109,8,9,1,
        9,1,9,1,10,3,10,114,8,10,1,10,1,10,1,10,1,10,1,10,3,10,121,8,10,
        1,10,1,10,3,10,125,8,10,1,11,1,11,1,12,1,12,1,12,5,12,132,8,12,10,
        12,12,12,135,9,12,1,13,3,13,138,8,13,1,13,1,13,1,13,1,14,1,14,1,
        14,5,14,146,8,14,10,14,12,14,149,9,14,1,15,1,15,1,15,1,15,1,15,1,
        15,1,15,1,15,1,15,1,15,3,15,161,8,15,1,16,1,16,1,16,1,16,1,16,1,
        16,1,16,1,16,1,16,3,16,172,8,16,1,16,1,16,1,16,1,16,1,16,1,16,1,
        16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,
        16,1,16,3,16,195,8,16,1,16,1,16,1,16,1,16,1,16,1,16,3,16,203,8,16,
        1,16,3,16,206,8,16,5,16,208,8,16,10,16,12,16,211,9,16,1,16,0,2,2,
        32,17,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,0,6,1,0,17,21,
        2,0,17,18,30,30,1,0,19,21,1,0,17,18,1,0,22,27,1,0,28,29,233,0,37,
        1,0,0,0,2,42,1,0,0,0,4,57,1,0,0,0,6,64,1,0,0,0,8,66,1,0,0,0,10,75,
        1,0,0,0,12,87,1,0,0,0,14,92,1,0,0,0,16,95,1,0,0,0,18,99,1,0,0,0,
        20,124,1,0,0,0,22,126,1,0,0,0,24,128,1,0,0,0,26,137,1,0,0,0,28,142,
        1,0,0,0,30,160,1,0,0,0,32,171,1,0,0,0,34,36,3,4,2,0,35,34,1,0,0,
        0,36,39,1,0,0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,40,1,0,0,0,39,37,
        1,0,0,0,40,41,5,0,0,1,41,1,1,0,0,0,42,43,6,1,-1,0,43,44,5,16,0,0,
        44,49,1,0,0,0,45,46,10,1,0,0,46,48,5,42,0,0,47,45,1,0,0,0,48,51,
        1,0,0,0,49,47,1,0,0,0,49,50,1,0,0,0,50,3,1,0,0,0,51,49,1,0,0,0,52,
        58,3,20,10,0,53,58,3,18,9,0,54,58,3,16,8,0,55,58,3,10,5,0,56,58,
        3,32,16,0,57,52,1,0,0,0,57,53,1,0,0,0,57,54,1,0,0,0,57,55,1,0,0,
        0,57,56,1,0,0,0,58,5,1,0,0,0,59,65,3,4,2,0,60,61,5,6,0,0,61,65,3,
        32,16,0,62,65,5,9,0,0,63,65,5,8,0,0,64,59,1,0,0,0,64,60,1,0,0,0,
        64,62,1,0,0,0,64,63,1,0,0,0,65,7,1,0,0,0,66,70,5,36,0,0,67,69,3,
        6,3,0,68,67,1,0,0,0,69,72,1,0,0,0,70,68,1,0,0,0,70,71,1,0,0,0,71,
        73,1,0,0,0,72,70,1,0,0,0,73,74,5,37,0,0,74,9,1,0,0,0,75,76,5,1,0,
        0,76,77,3,32,16,0,77,81,3,8,4,0,78,80,3,12,6,0,79,78,1,0,0,0,80,
        83,1,0,0,0,81,79,1,0,0,0,81,82,1,0,0,0,82,85,1,0,0,0,83,81,1,0,0,
        0,84,86,3,14,7,0,85,84,1,0,0,0,85,86,1,0,0,0,86,11,1,0,0,0,87,88,
        5,4,0,0,88,89,5,1,0,0,89,90,3,32,16,0,90,91,3,8,4,0,91,13,1,0,0,
        0,92,93,5,4,0,0,93,94,3,8,4,0,94,15,1,0,0,0,95,96,5,7,0,0,96,97,
        3,32,16,0,97,98,3,8,4,0,98,17,1,0,0,0,99,100,5,3,0,0,100,101,5,16,
        0,0,101,103,5,34,0,0,102,104,3,28,14,0,103,102,1,0,0,0,103,104,1,
        0,0,0,104,105,1,0,0,0,105,108,5,35,0,0,106,107,5,41,0,0,107,109,
        3,2,1,0,108,106,1,0,0,0,108,109,1,0,0,0,109,110,1,0,0,0,110,111,
        3,8,4,0,111,19,1,0,0,0,112,114,5,5,0,0,113,112,1,0,0,0,113,114,1,
        0,0,0,114,115,1,0,0,0,115,116,5,16,0,0,116,117,5,33,0,0,117,125,
        3,32,16,0,118,120,5,16,0,0,119,121,7,0,0,0,120,119,1,0,0,0,120,121,
        1,0,0,0,121,122,1,0,0,0,122,123,5,33,0,0,123,125,3,32,16,0,124,113,
        1,0,0,0,124,118,1,0,0,0,125,21,1,0,0,0,126,127,3,32,16,0,127,23,
        1,0,0,0,128,133,3,22,11,0,129,130,5,32,0,0,130,132,3,22,11,0,131,
        129,1,0,0,0,132,135,1,0,0,0,133,131,1,0,0,0,133,134,1,0,0,0,134,
        25,1,0,0,0,135,133,1,0,0,0,136,138,5,5,0,0,137,136,1,0,0,0,137,138,
        1,0,0,0,138,139,1,0,0,0,139,140,3,2,1,0,140,141,5,16,0,0,141,27,
        1,0,0,0,142,147,3,26,13,0,143,144,5,32,0,0,144,146,3,26,13,0,145,
        143,1,0,0,0,146,149,1,0,0,0,147,145,1,0,0,0,147,148,1,0,0,0,148,
        29,1,0,0,0,149,147,1,0,0,0,150,161,5,11,0,0,151,161,5,12,0,0,152,
        161,5,13,0,0,153,161,5,14,0,0,154,161,5,15,0,0,155,161,5,16,0,0,
        156,157,5,34,0,0,157,158,3,32,16,0,158,159,5,35,0,0,159,161,1,0,
        0,0,160,150,1,0,0,0,160,151,1,0,0,0,160,152,1,0,0,0,160,153,1,0,
        0,0,160,154,1,0,0,0,160,155,1,0,0,0,160,156,1,0,0,0,161,31,1,0,0,
        0,162,163,6,16,-1,0,163,164,5,34,0,0,164,165,3,2,1,0,165,166,5,35,
        0,0,166,167,3,32,16,10,167,172,1,0,0,0,168,172,3,30,15,0,169,170,
        7,1,0,0,170,172,3,32,16,1,171,162,1,0,0,0,171,168,1,0,0,0,171,169,
        1,0,0,0,172,209,1,0,0,0,173,174,10,6,0,0,174,175,5,1,0,0,175,176,
        3,32,16,0,176,177,5,4,0,0,177,178,3,32,16,7,178,208,1,0,0,0,179,
        180,10,5,0,0,180,181,7,2,0,0,181,208,3,32,16,6,182,183,10,4,0,0,
        183,184,7,3,0,0,184,208,3,32,16,5,185,186,10,3,0,0,186,187,7,4,0,
        0,187,208,3,32,16,4,188,189,10,2,0,0,189,190,7,5,0,0,190,208,3,32,
        16,3,191,192,10,8,0,0,192,194,5,34,0,0,193,195,3,24,12,0,194,193,
        1,0,0,0,194,195,1,0,0,0,195,196,1,0,0,0,196,208,5,35,0,0,197,198,
        10,7,0,0,198,199,5,31,0,0,199,205,5,16,0,0,200,202,5,34,0,0,201,
        203,3,24,12,0,202,201,1,0,0,0,202,203,1,0,0,0,203,204,1,0,0,0,204,
        206,5,35,0,0,205,200,1,0,0,0,205,206,1,0,0,0,206,208,1,0,0,0,207,
        173,1,0,0,0,207,179,1,0,0,0,207,182,1,0,0,0,207,185,1,0,0,0,207,
        188,1,0,0,0,207,191,1,0,0,0,207,197,1,0,0,0,208,211,1,0,0,0,209,
        207,1,0,0,0,209,210,1,0,0,0,210,33,1,0,0,0,211,209,1,0,0,0,22,37,
        49,57,64,70,81,85,103,108,113,120,124,133,137,147,160,171,194,202,
        205,207,209
    ]

class CureParser ( Parser ):

    grammarFileName = "Cure.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'new'", "'fn'", "'else'", "'mut'", 
                     "'return'", "'while'", "'break'", "'continue'", "'''", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'nil'", "<INVALID>", "'+'", "'-'", "'*'", "'/'", "'%'", 
                     "'=='", "'!='", "'>'", "'<'", "'>='", "'<='", "'&&'", 
                     "'||'", "'!'", "'.'", "','", "'='", "'('", "')'", "'{'", 
                     "'}'", "'['", "']'", "'<-'", "'->'", "'&'" ]

    symbolicNames = [ "<INVALID>", "IF", "NEW", "FUNC", "ELSE", "MUTABLE", 
                      "RETURN", "WHILE", "BREAK", "CONTINUE", "APOSTROPHE", 
                      "INT", "FLOAT", "STRING", "BOOL", "NIL", "ID", "ADD", 
                      "SUB", "MUL", "DIV", "MOD", "EEQ", "NEQ", "GT", "LT", 
                      "GTE", "LTE", "AND", "OR", "NOT", "DOT", "COMMA", 
                      "ASSIGN", "LPAREN", "RPAREN", "LBRACE", "RBRACE", 
                      "LBRACK", "RBRACK", "RARROW", "RETURNS", "AMPERSAND", 
                      "COMMENT", "MULTILINE_COMMENT", "WHITESPACE", "OTHER" ]

    RULE_parse = 0
    RULE_type = 1
    RULE_stmt = 2
    RULE_bodyStmts = 3
    RULE_body = 4
    RULE_ifStmt = 5
    RULE_elseifStmt = 6
    RULE_elseStmt = 7
    RULE_whileStmt = 8
    RULE_funcAssign = 9
    RULE_varAssign = 10
    RULE_arg = 11
    RULE_args = 12
    RULE_param = 13
    RULE_params = 14
    RULE_atom = 15
    RULE_expr = 16

    ruleNames =  [ "parse", "type", "stmt", "bodyStmts", "body", "ifStmt", 
                   "elseifStmt", "elseStmt", "whileStmt", "funcAssign", 
                   "varAssign", "arg", "args", "param", "params", "atom", 
                   "expr" ]

    EOF = Token.EOF
    IF=1
    NEW=2
    FUNC=3
    ELSE=4
    MUTABLE=5
    RETURN=6
    WHILE=7
    BREAK=8
    CONTINUE=9
    APOSTROPHE=10
    INT=11
    FLOAT=12
    STRING=13
    BOOL=14
    NIL=15
    ID=16
    ADD=17
    SUB=18
    MUL=19
    DIV=20
    MOD=21
    EEQ=22
    NEQ=23
    GT=24
    LT=25
    GTE=26
    LTE=27
    AND=28
    OR=29
    NOT=30
    DOT=31
    COMMA=32
    ASSIGN=33
    LPAREN=34
    RPAREN=35
    LBRACE=36
    RBRACE=37
    LBRACK=38
    RBRACK=39
    RARROW=40
    RETURNS=41
    AMPERSAND=42
    COMMENT=43
    MULTILINE_COMMENT=44
    WHITESPACE=45
    OTHER=46

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ParseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(CureParser.EOF, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.StmtContext)
            else:
                return self.getTypedRuleContext(CureParser.StmtContext,i)


        def getRuleIndex(self):
            return CureParser.RULE_parse

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParse" ):
                return visitor.visitParse(self)
            else:
                return visitor.visitChildren(self)




    def parse(self):

        localctx = CureParser.ParseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_parse)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18254133418) != 0):
                self.state = 34
                self.stmt()
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 40
            self.match(CureParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def AMPERSAND(self):
            return self.getToken(CureParser.AMPERSAND, 0)

        def getRuleIndex(self):
            return CureParser.RULE_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)



    def type_(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CureParser.TypeContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_type, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.match(CureParser.ID)
            self._ctx.stop = self._input.LT(-1)
            self.state = 49
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = CureParser.TypeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_type)
                    self.state = 45
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 46
                    self.match(CureParser.AMPERSAND) 
                self.state = 51
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varAssign(self):
            return self.getTypedRuleContext(CureParser.VarAssignContext,0)


        def funcAssign(self):
            return self.getTypedRuleContext(CureParser.FuncAssignContext,0)


        def whileStmt(self):
            return self.getTypedRuleContext(CureParser.WhileStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(CureParser.IfStmtContext,0)


        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = CureParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        try:
            self.state = 57
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 52
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 53
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 54
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 55
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 56
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyStmtsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self):
            return self.getTypedRuleContext(CureParser.StmtContext,0)


        def RETURN(self):
            return self.getToken(CureParser.RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def CONTINUE(self):
            return self.getToken(CureParser.CONTINUE, 0)

        def BREAK(self):
            return self.getToken(CureParser.BREAK, 0)

        def getRuleIndex(self):
            return CureParser.RULE_bodyStmts

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBodyStmts" ):
                return visitor.visitBodyStmts(self)
            else:
                return visitor.visitChildren(self)




    def bodyStmts(self):

        localctx = CureParser.BodyStmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_bodyStmts)
        try:
            self.state = 64
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 5, 7, 11, 12, 13, 14, 15, 16, 17, 18, 30, 34]:
                self.enterOuterAlt(localctx, 1)
                self.state = 59
                self.stmt()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 60
                self.match(CureParser.RETURN)
                self.state = 61
                self.expr(0)
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 62
                self.match(CureParser.CONTINUE)
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 4)
                self.state = 63
                self.match(CureParser.BREAK)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(CureParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(CureParser.RBRACE, 0)

        def bodyStmts(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.BodyStmtsContext)
            else:
                return self.getTypedRuleContext(CureParser.BodyStmtsContext,i)


        def getRuleIndex(self):
            return CureParser.RULE_body

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = CureParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(CureParser.LBRACE)
            self.state = 70
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18254134250) != 0):
                self.state = 67
                self.bodyStmts()
                self.state = 72
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 73
            self.match(CureParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(CureParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def elseifStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ElseifStmtContext)
            else:
                return self.getTypedRuleContext(CureParser.ElseifStmtContext,i)


        def elseStmt(self):
            return self.getTypedRuleContext(CureParser.ElseStmtContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_ifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = CureParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(CureParser.IF)
            self.state = 76
            self.expr(0)
            self.state = 77
            self.body()
            self.state = 81
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 78
                    self.elseifStmt() 
                self.state = 83
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 84
                self.elseStmt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseifStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(CureParser.ELSE, 0)

        def IF(self):
            return self.getToken(CureParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_elseifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseifStmt" ):
                return visitor.visitElseifStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseifStmt(self):

        localctx = CureParser.ElseifStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_elseifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.match(CureParser.ELSE)
            self.state = 88
            self.match(CureParser.IF)
            self.state = 89
            self.expr(0)
            self.state = 90
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(CureParser.ELSE, 0)

        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_elseStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseStmt" ):
                return visitor.visitElseStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseStmt(self):

        localctx = CureParser.ElseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_elseStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self.match(CureParser.ELSE)
            self.state = 93
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(CureParser.WHILE, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_whileStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = CureParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.match(CureParser.WHILE)
            self.state = 96
            self.expr(0)
            self.state = 97
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNC(self):
            return self.getToken(CureParser.FUNC, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def body(self):
            return self.getTypedRuleContext(CureParser.BodyContext,0)


        def params(self):
            return self.getTypedRuleContext(CureParser.ParamsContext,0)


        def RETURNS(self):
            return self.getToken(CureParser.RETURNS, 0)

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_funcAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncAssign" ):
                return visitor.visitFuncAssign(self)
            else:
                return visitor.visitChildren(self)




    def funcAssign(self):

        localctx = CureParser.FuncAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_funcAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(CureParser.FUNC)
            self.state = 100
            self.match(CureParser.ID)
            self.state = 101
            self.match(CureParser.LPAREN)
            self.state = 103
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5 or _la==16:
                self.state = 102
                self.params()


            self.state = 105
            self.match(CureParser.RPAREN)
            self.state = 108
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 106
                self.match(CureParser.RETURNS)
                self.state = 107
                self.type_(0)


            self.state = 110
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(CureParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def MUTABLE(self):
            return self.getToken(CureParser.MUTABLE, 0)

        def ADD(self):
            return self.getToken(CureParser.ADD, 0)

        def SUB(self):
            return self.getToken(CureParser.SUB, 0)

        def MUL(self):
            return self.getToken(CureParser.MUL, 0)

        def DIV(self):
            return self.getToken(CureParser.DIV, 0)

        def MOD(self):
            return self.getToken(CureParser.MOD, 0)

        def getRuleIndex(self):
            return CureParser.RULE_varAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarAssign" ):
                return visitor.visitVarAssign(self)
            else:
                return visitor.visitChildren(self)




    def varAssign(self):

        localctx = CureParser.VarAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_varAssign)
        self._la = 0 # Token type
        try:
            self.state = 124
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 113
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==5:
                    self.state = 112
                    self.match(CureParser.MUTABLE)


                self.state = 115
                self.match(CureParser.ID)
                self.state = 116
                self.match(CureParser.ASSIGN)
                self.state = 117
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 118
                self.match(CureParser.ID)
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 4063232) != 0):
                    self.state = 119
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4063232) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 122
                self.match(CureParser.ASSIGN)
                self.state = 123
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def getRuleIndex(self):
            return CureParser.RULE_arg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg" ):
                return visitor.visitArg(self)
            else:
                return visitor.visitChildren(self)




    def arg(self):

        localctx = CureParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ArgContext)
            else:
                return self.getTypedRuleContext(CureParser.ArgContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CureParser.COMMA)
            else:
                return self.getToken(CureParser.COMMA, i)

        def getRuleIndex(self):
            return CureParser.RULE_args

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgs" ):
                return visitor.visitArgs(self)
            else:
                return visitor.visitChildren(self)




    def args(self):

        localctx = CureParser.ArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.arg()
            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 129
                self.match(CureParser.COMMA)
                self.state = 130
                self.arg()
                self.state = 135
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)


        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def MUTABLE(self):
            return self.getToken(CureParser.MUTABLE, 0)

        def getRuleIndex(self):
            return CureParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = CureParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 136
                self.match(CureParser.MUTABLE)


            self.state = 139
            self.type_(0)
            self.state = 140
            self.match(CureParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ParamContext)
            else:
                return self.getTypedRuleContext(CureParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(CureParser.COMMA)
            else:
                return self.getToken(CureParser.COMMA, i)

        def getRuleIndex(self):
            return CureParser.RULE_params

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParams" ):
                return visitor.visitParams(self)
            else:
                return visitor.visitChildren(self)




    def params(self):

        localctx = CureParser.ParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.param()
            self.state = 147
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 143
                self.match(CureParser.COMMA)
                self.state = 144
                self.param()
                self.state = 149
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(CureParser.INT, 0)

        def FLOAT(self):
            return self.getToken(CureParser.FLOAT, 0)

        def STRING(self):
            return self.getToken(CureParser.STRING, 0)

        def BOOL(self):
            return self.getToken(CureParser.BOOL, 0)

        def NIL(self):
            return self.getToken(CureParser.NIL, 0)

        def ID(self):
            return self.getToken(CureParser.ID, 0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)

        def getRuleIndex(self):
            return CureParser.RULE_atom

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = CureParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_atom)
        try:
            self.state = 160
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 150
                self.match(CureParser.INT)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 151
                self.match(CureParser.FLOAT)
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 3)
                self.state = 152
                self.match(CureParser.STRING)
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 4)
                self.state = 153
                self.match(CureParser.BOOL)
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 5)
                self.state = 154
                self.match(CureParser.NIL)
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 6)
                self.state = 155
                self.match(CureParser.ID)
                pass
            elif token in [34]:
                self.enterOuterAlt(localctx, 7)
                self.state = 156
                self.match(CureParser.LPAREN)
                self.state = 157
                self.expr(0)
                self.state = 158
                self.match(CureParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CureParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class CallContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall" ):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)


    class CastContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)
        def type_(self):
            return self.getTypedRuleContext(CureParser.TypeContext,0)

        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCast" ):
                return visitor.visitCast(self)
            else:
                return visitor.visitChildren(self)


    class Atom_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(CureParser.AtomContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom_expr" ):
                return visitor.visitAtom_expr(self)
            else:
                return visitor.visitChildren(self)


    class RelationalContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def EEQ(self):
            return self.getToken(CureParser.EEQ, 0)
        def NEQ(self):
            return self.getToken(CureParser.NEQ, 0)
        def GT(self):
            return self.getToken(CureParser.GT, 0)
        def LT(self):
            return self.getToken(CureParser.LT, 0)
        def GTE(self):
            return self.getToken(CureParser.GTE, 0)
        def LTE(self):
            return self.getToken(CureParser.LTE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelational" ):
                return visitor.visitRelational(self)
            else:
                return visitor.visitChildren(self)


    class UnaryContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.uop = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)

        def NOT(self):
            return self.getToken(CureParser.NOT, 0)
        def SUB(self):
            return self.getToken(CureParser.SUB, 0)
        def ADD(self):
            return self.getToken(CureParser.ADD, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnary" ):
                return visitor.visitUnary(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicationContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def MUL(self):
            return self.getToken(CureParser.MUL, 0)
        def DIV(self):
            return self.getToken(CureParser.DIV, 0)
        def MOD(self):
            return self.getToken(CureParser.MOD, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplication" ):
                return visitor.visitMultiplication(self)
            else:
                return visitor.visitChildren(self)


    class AttrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CureParser.ExprContext,0)

        def DOT(self):
            return self.getToken(CureParser.DOT, 0)
        def ID(self):
            return self.getToken(CureParser.ID, 0)
        def LPAREN(self):
            return self.getToken(CureParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(CureParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(CureParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr" ):
                return visitor.visitAttr(self)
            else:
                return visitor.visitChildren(self)


    class TernaryContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def IF(self):
            return self.getToken(CureParser.IF, 0)
        def ELSE(self):
            return self.getToken(CureParser.ELSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTernary" ):
                return visitor.visitTernary(self)
            else:
                return visitor.visitChildren(self)


    class LogicalContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def AND(self):
            return self.getToken(CureParser.AND, 0)
        def OR(self):
            return self.getToken(CureParser.OR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogical" ):
                return visitor.visitLogical(self)
            else:
                return visitor.visitChildren(self)


    class AdditionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CureParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CureParser.ExprContext)
            else:
                return self.getTypedRuleContext(CureParser.ExprContext,i)

        def ADD(self):
            return self.getToken(CureParser.ADD, 0)
        def SUB(self):
            return self.getToken(CureParser.SUB, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddition" ):
                return visitor.visitAddition(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CureParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 32
        self.enterRecursionRule(localctx, 32, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                localctx = CureParser.CastContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 163
                self.match(CureParser.LPAREN)
                self.state = 164
                self.type_(0)
                self.state = 165
                self.match(CureParser.RPAREN)
                self.state = 166
                self.expr(10)
                pass

            elif la_ == 2:
                localctx = CureParser.Atom_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 168
                self.atom()
                pass

            elif la_ == 3:
                localctx = CureParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 169
                localctx.uop = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1074135040) != 0)):
                    localctx.uop = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 170
                self.expr(1)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 209
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,21,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 207
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
                    if la_ == 1:
                        localctx = CureParser.TernaryContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 173
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 174
                        self.match(CureParser.IF)
                        self.state = 175
                        self.expr(0)
                        self.state = 176
                        self.match(CureParser.ELSE)
                        self.state = 177
                        self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = CureParser.MultiplicationContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 179
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 180
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3670016) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 181
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = CureParser.AdditionContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 182
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 183
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==17 or _la==18):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 184
                        self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = CureParser.RelationalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 185
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 186
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 264241152) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 187
                        self.expr(4)
                        pass

                    elif la_ == 5:
                        localctx = CureParser.LogicalContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 188
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 189
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==28 or _la==29):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 190
                        self.expr(3)
                        pass

                    elif la_ == 6:
                        localctx = CureParser.CallContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 191
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 192
                        self.match(CureParser.LPAREN)
                        self.state = 194
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 18254133248) != 0):
                            self.state = 193
                            self.args()


                        self.state = 196
                        self.match(CureParser.RPAREN)
                        pass

                    elif la_ == 7:
                        localctx = CureParser.AttrContext(self, CureParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 197
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 198
                        self.match(CureParser.DOT)
                        self.state = 199
                        self.match(CureParser.ID)
                        self.state = 205
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
                        if la_ == 1:
                            self.state = 200
                            self.match(CureParser.LPAREN)
                            self.state = 202
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 18254133248) != 0):
                                self.state = 201
                                self.args()


                            self.state = 204
                            self.match(CureParser.RPAREN)


                        pass

             
                self.state = 211
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,21,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.type_sempred
        self._predicates[16] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def type_sempred(self, localctx:TypeContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 7)
         




