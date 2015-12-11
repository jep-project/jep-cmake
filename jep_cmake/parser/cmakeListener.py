# Generated from D:/Work/jep/src/jep-cmake/grammar\cmake.g4 by ANTLR 4.5.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .cmakeParser import cmakeParser
else:
    from cmakeParser import cmakeParser

# This class defines a complete listener for a parse tree produced by cmakeParser.
class cmakeListener(ParseTreeListener):

    # Enter a parse tree produced by cmakeParser#file.
    def enterFile(self, ctx:cmakeParser.FileContext):
        pass

    # Exit a parse tree produced by cmakeParser#file.
    def exitFile(self, ctx:cmakeParser.FileContext):
        pass


    # Enter a parse tree produced by cmakeParser#row.
    def enterRow(self, ctx:cmakeParser.RowContext):
        pass

    # Exit a parse tree produced by cmakeParser#row.
    def exitRow(self, ctx:cmakeParser.RowContext):
        pass


    # Enter a parse tree produced by cmakeParser#field.
    def enterField(self, ctx:cmakeParser.FieldContext):
        pass

    # Exit a parse tree produced by cmakeParser#field.
    def exitField(self, ctx:cmakeParser.FieldContext):
        pass


