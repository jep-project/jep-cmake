"""CMake abstract syntax tree, kept minimal for supported use cases. Independent of used parser library."""
import logging


class CompilationUnit:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.fileelements = []

    def __repr__(self):
        return 'CompilationUnit({!r})'.format(self.filepath)


class CommandDefinition:
    def __init__(self, name: str = None):
        self.name = name

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.name)


class FunctionDefinition(CommandDefinition):
    pass


class MacroDefinition(CommandDefinition):
    pass
