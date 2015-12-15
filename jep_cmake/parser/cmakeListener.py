# Generated from D:/Work/jep/src/jep-cmake/grammar\cmake.g4 by ANTLR 4.5.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .cmakeParser import cmakeParser
else:
    from cmakeParser import cmakeParser

# This class defines a complete listener for a parse tree produced by cmakeParser.
class cmakeListener(ParseTreeListener):

    # Enter a parse tree produced by cmakeParser#compilationUnit.
    def enterCompilationUnit(self, ctx:cmakeParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by cmakeParser#compilationUnit.
    def exitCompilationUnit(self, ctx:cmakeParser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by cmakeParser#fileElement.
    def enterFileElement(self, ctx:cmakeParser.FileElementContext):
        pass

    # Exit a parse tree produced by cmakeParser#fileElement.
    def exitFileElement(self, ctx:cmakeParser.FileElementContext):
        pass


    # Enter a parse tree produced by cmakeParser#commandInvocation.
    def enterCommandInvocation(self, ctx:cmakeParser.CommandInvocationContext):
        pass

    # Exit a parse tree produced by cmakeParser#commandInvocation.
    def exitCommandInvocation(self, ctx:cmakeParser.CommandInvocationContext):
        pass


    # Enter a parse tree produced by cmakeParser#groupedArguments.
    def enterGroupedArguments(self, ctx:cmakeParser.GroupedArgumentsContext):
        pass

    # Exit a parse tree produced by cmakeParser#groupedArguments.
    def exitGroupedArguments(self, ctx:cmakeParser.GroupedArgumentsContext):
        pass


    # Enter a parse tree produced by cmakeParser#argument.
    def enterArgument(self, ctx:cmakeParser.ArgumentContext):
        pass

    # Exit a parse tree produced by cmakeParser#argument.
    def exitArgument(self, ctx:cmakeParser.ArgumentContext):
        pass


