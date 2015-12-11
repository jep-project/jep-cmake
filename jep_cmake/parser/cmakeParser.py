# Generated from D:/Work/jep/src/jep-cmake/grammar\cmake.g4 by ANTLR 4.5.1
# encoding: utf-8
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\6")
        buf.write("\33\4\2\t\2\4\3\t\3\4\4\t\4\3\2\6\2\n\n\2\r\2\16\2\13")
        buf.write("\3\2\3\2\3\3\3\3\3\3\3\3\5\3\24\n\3\3\3\3\3\3\3\3\4\3")
        buf.write("\4\3\4\2\2\5\2\4\6\2\2\31\2\t\3\2\2\2\4\17\3\2\2\2\6\30")
        buf.write("\3\2\2\2\b\n\5\4\3\2\t\b\3\2\2\2\n\13\3\2\2\2\13\t\3\2")
        buf.write("\2\2\13\f\3\2\2\2\f\r\3\2\2\2\r\16\b\2\1\2\16\3\3\2\2")
        buf.write("\2\17\20\5\6\4\2\20\21\7\3\2\2\21\23\5\6\4\2\22\24\7\4")
        buf.write("\2\2\23\22\3\2\2\2\23\24\3\2\2\2\24\25\3\2\2\2\25\26\7")
        buf.write("\5\2\2\26\27\b\3\1\2\27\5\3\2\2\2\30\31\7\6\2\2\31\7\3")
        buf.write("\2\2\2\4\13\23")
        return buf.getvalue()


class cmakeParser ( Parser ):

    grammarFileName = "cmake.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','", "'\r'", "'\n'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "TEXT" ]

    RULE_file = 0
    RULE_row = 1
    RULE_field = 2

    ruleNames =  [ "file", "row", "field" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    TEXT=4

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.5.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    double x, y; // keep column sums in these fields


    class FileContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def row(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(cmakeParser.RowContext)
            else:
                return self.getTypedRuleContext(cmakeParser.RowContext,i)


        def getRuleIndex(self):
            return cmakeParser.RULE_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile" ):
                listener.enterFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile" ):
                listener.exitFile(self)




    def file(self):

        localctx = cmakeParser.FileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_file)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 7 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 6
                self.row()
                self.state = 9 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==cmakeParser.TEXT):
                    break

            System.out.printf("%f, %f\n", x, y);
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RowContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.a = None # FieldContext
            self.b = None # FieldContext

        def field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(cmakeParser.FieldContext)
            else:
                return self.getTypedRuleContext(cmakeParser.FieldContext,i)


        def getRuleIndex(self):
            return cmakeParser.RULE_row

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRow" ):
                listener.enterRow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRow" ):
                listener.exitRow(self)




    def row(self):

        localctx = cmakeParser.RowContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_row)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            localctx.a = self.field()
            self.state = 14
            self.match(cmakeParser.T__0)
            self.state = 15
            localctx.b = self.field()
            self.state = 17
            _la = self._input.LA(1)
            if _la==cmakeParser.T__1:
                self.state = 16
                self.match(cmakeParser.T__1)


            self.state = 19
            self.match(cmakeParser.T__2)

                  x += Double.valueOf((None if localctx.a is None else localctx.a.start).getText());
                  y += Double.valueOf((None if localctx.b is None else localctx.b.start).getText());
                  
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FieldContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TEXT(self):
            return self.getToken(cmakeParser.TEXT, 0)

        def getRuleIndex(self):
            return cmakeParser.RULE_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField" ):
                listener.enterField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField" ):
                listener.exitField(self)




    def field(self):

        localctx = cmakeParser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_field)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.match(cmakeParser.TEXT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





