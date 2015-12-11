# Generated from D:/Work/jep/src/jep-cmake/grammar\cmake.g4 by ANTLR 4.5.1
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2\6")
        buf.write("\26\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\3\3")
        buf.write("\3\3\4\3\4\3\5\6\5\23\n\5\r\5\16\5\24\2\2\6\3\3\5\4\7")
        buf.write("\5\t\6\3\2\3\5\2\f\f\17\17..\26\2\3\3\2\2\2\2\5\3\2\2")
        buf.write("\2\2\7\3\2\2\2\2\t\3\2\2\2\3\13\3\2\2\2\5\r\3\2\2\2\7")
        buf.write("\17\3\2\2\2\t\22\3\2\2\2\13\f\7.\2\2\f\4\3\2\2\2\r\16")
        buf.write("\7\17\2\2\16\6\3\2\2\2\17\20\7\f\2\2\20\b\3\2\2\2\21\23")
        buf.write("\n\2\2\2\22\21\3\2\2\2\23\24\3\2\2\2\24\22\3\2\2\2\24")
        buf.write("\25\3\2\2\2\25\n\3\2\2\2\4\2\24\2")
        return buf.getvalue()


class cmakeLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    T__0 = 1
    T__1 = 2
    T__2 = 3
    TEXT = 4

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "','", "'\r'", "'\n'" ]

    symbolicNames = [ "<INVALID>",
            "TEXT" ]

    ruleNames = [ "T__0", "T__1", "T__2", "TEXT" ]

    grammarFileName = "cmake.g4"

    def __init__(self, input=None):
        super().__init__(input)
        self.checkVersion("4.5.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    double x, y; // keep column sums in these fields


