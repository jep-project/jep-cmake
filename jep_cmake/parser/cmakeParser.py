# Generated from D:/Work/jep/src/jep-cmake/grammar\cmake.g4 by ANTLR 4.5.1
# encoding: utf-8
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\b")
        buf.write("\'\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\7\2\16")
        buf.write("\n\2\f\2\16\2\21\13\2\3\3\3\3\3\4\3\4\3\4\3\5\3\5\7\5")
        buf.write("\32\n\5\f\5\16\5\35\13\5\3\5\3\5\3\6\3\6\3\6\3\6\5\6%")
        buf.write("\n\6\3\6\2\2\7\2\4\6\b\n\2\2&\2\17\3\2\2\2\4\22\3\2\2")
        buf.write("\2\6\24\3\2\2\2\b\27\3\2\2\2\n$\3\2\2\2\f\16\5\4\3\2\r")
        buf.write("\f\3\2\2\2\16\21\3\2\2\2\17\r\3\2\2\2\17\20\3\2\2\2\20")
        buf.write("\3\3\2\2\2\21\17\3\2\2\2\22\23\5\6\4\2\23\5\3\2\2\2\24")
        buf.write("\25\7\5\2\2\25\26\5\b\5\2\26\7\3\2\2\2\27\33\7\3\2\2\30")
        buf.write("\32\5\n\6\2\31\30\3\2\2\2\32\35\3\2\2\2\33\31\3\2\2\2")
        buf.write("\33\34\3\2\2\2\34\36\3\2\2\2\35\33\3\2\2\2\36\37\7\4\2")
        buf.write("\2\37\t\3\2\2\2 %\7\7\2\2!%\7\6\2\2\"%\7\5\2\2#%\5\b\5")
        buf.write("\2$ \3\2\2\2$!\3\2\2\2$\"\3\2\2\2$#\3\2\2\2%\13\3\2\2")
        buf.write("\2\5\17\33$")
        return buf.getvalue()


class cmakeParser ( Parser ):

    grammarFileName = "cmake.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "IDENTIFIER", 
                      "UNQUOTED_ARGUMENT", "QUOTED_ARGUMENT", "SKIP" ]

    RULE_compilation_unit = 0
    RULE_file_element = 1
    RULE_command_invocation = 2
    RULE_grouped_arguments = 3
    RULE_argument = 4

    ruleNames =  [ "compilation_unit", "file_element", "command_invocation", 
                   "grouped_arguments", "argument" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    IDENTIFIER=3
    UNQUOTED_ARGUMENT=4
    QUOTED_ARGUMENT=5
    SKIP=6

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.5.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class Compilation_unitContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def file_element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(cmakeParser.File_elementContext)
            else:
                return self.getTypedRuleContext(cmakeParser.File_elementContext,i)


        def getRuleIndex(self):
            return cmakeParser.RULE_compilation_unit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompilation_unit" ):
                listener.enterCompilation_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompilation_unit" ):
                listener.exitCompilation_unit(self)




    def compilation_unit(self):

        localctx = cmakeParser.Compilation_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_compilation_unit)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==cmakeParser.IDENTIFIER:
                self.state = 10
                self.file_element()
                self.state = 15
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class File_elementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def command_invocation(self):
            return self.getTypedRuleContext(cmakeParser.Command_invocationContext,0)


        def getRuleIndex(self):
            return cmakeParser.RULE_file_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile_element" ):
                listener.enterFile_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile_element" ):
                listener.exitFile_element(self)




    def file_element(self):

        localctx = cmakeParser.File_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_file_element)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 16
            self.command_invocation()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Command_invocationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.command = None # Token

        def grouped_arguments(self):
            return self.getTypedRuleContext(cmakeParser.Grouped_argumentsContext,0)


        def IDENTIFIER(self):
            return self.getToken(cmakeParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return cmakeParser.RULE_command_invocation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommand_invocation" ):
                listener.enterCommand_invocation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommand_invocation" ):
                listener.exitCommand_invocation(self)




    def command_invocation(self):

        localctx = cmakeParser.Command_invocationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_command_invocation)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18
            localctx.command = self.match(cmakeParser.IDENTIFIER)
            self.state = 19
            self.grouped_arguments()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Grouped_argumentsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(cmakeParser.ArgumentContext)
            else:
                return self.getTypedRuleContext(cmakeParser.ArgumentContext,i)


        def getRuleIndex(self):
            return cmakeParser.RULE_grouped_arguments

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGrouped_arguments" ):
                listener.enterGrouped_arguments(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGrouped_arguments" ):
                listener.exitGrouped_arguments(self)




    def grouped_arguments(self):

        localctx = cmakeParser.Grouped_argumentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_grouped_arguments)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 21
            self.match(cmakeParser.T__0)
            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << cmakeParser.T__0) | (1 << cmakeParser.IDENTIFIER) | (1 << cmakeParser.UNQUOTED_ARGUMENT) | (1 << cmakeParser.QUOTED_ARGUMENT))) != 0):
                self.state = 22
                self.argument()
                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 28
            self.match(cmakeParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgumentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTED_ARGUMENT(self):
            return self.getToken(cmakeParser.QUOTED_ARGUMENT, 0)

        def UNQUOTED_ARGUMENT(self):
            return self.getToken(cmakeParser.UNQUOTED_ARGUMENT, 0)

        def IDENTIFIER(self):
            return self.getToken(cmakeParser.IDENTIFIER, 0)

        def grouped_arguments(self):
            return self.getTypedRuleContext(cmakeParser.Grouped_argumentsContext,0)


        def getRuleIndex(self):
            return cmakeParser.RULE_argument

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgument" ):
                listener.enterArgument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgument" ):
                listener.exitArgument(self)




    def argument(self):

        localctx = cmakeParser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_argument)
        try:
            self.state = 34
            token = self._input.LA(1)
            if token in [cmakeParser.QUOTED_ARGUMENT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 30
                self.match(cmakeParser.QUOTED_ARGUMENT)

            elif token in [cmakeParser.UNQUOTED_ARGUMENT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 31
                self.match(cmakeParser.UNQUOTED_ARGUMENT)

            elif token in [cmakeParser.IDENTIFIER]:
                self.enterOuterAlt(localctx, 3)
                self.state = 32
                self.match(cmakeParser.IDENTIFIER)

            elif token in [cmakeParser.T__0]:
                self.enterOuterAlt(localctx, 4)
                self.state = 33
                self.grouped_arguments()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





