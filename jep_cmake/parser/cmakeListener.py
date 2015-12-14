# Generated from D:/Work/jep/src/jep-cmake/grammar\cmake.g4 by ANTLR 4.5.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .cmakeParser import cmakeParser
else:
    from cmakeParser import cmakeParser

# This class defines a complete listener for a parse tree produced by cmakeParser.
class cmakeListener(ParseTreeListener):

    # Enter a parse tree produced by cmakeParser#compilation_unit.
    def enterCompilation_unit(self, ctx:cmakeParser.Compilation_unitContext):
        pass

    # Exit a parse tree produced by cmakeParser#compilation_unit.
    def exitCompilation_unit(self, ctx:cmakeParser.Compilation_unitContext):
        pass


    # Enter a parse tree produced by cmakeParser#file_element.
    def enterFile_element(self, ctx:cmakeParser.File_elementContext):
        pass

    # Exit a parse tree produced by cmakeParser#file_element.
    def exitFile_element(self, ctx:cmakeParser.File_elementContext):
        pass


    # Enter a parse tree produced by cmakeParser#command_invocation.
    def enterCommand_invocation(self, ctx:cmakeParser.Command_invocationContext):
        pass

    # Exit a parse tree produced by cmakeParser#command_invocation.
    def exitCommand_invocation(self, ctx:cmakeParser.Command_invocationContext):
        pass


    # Enter a parse tree produced by cmakeParser#grouped_arguments.
    def enterGrouped_arguments(self, ctx:cmakeParser.Grouped_argumentsContext):
        pass

    # Exit a parse tree produced by cmakeParser#grouped_arguments.
    def exitGrouped_arguments(self, ctx:cmakeParser.Grouped_argumentsContext):
        pass


    # Enter a parse tree produced by cmakeParser#argument.
    def enterArgument(self, ctx:cmakeParser.ArgumentContext):
        pass

    # Exit a parse tree produced by cmakeParser#argument.
    def exitArgument(self, ctx:cmakeParser.ArgumentContext):
        pass


