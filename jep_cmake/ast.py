"""CMake abstract syntax tree, kept minimal for supported use cases. Independent of used parser library."""
import logging


class CompilationUnit:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.fileelements = []

    def __repr__(self):
        return 'CompilationUnit({!r})'.format(self.filepath)


class CommandDefinition:
    def __init__(self, name: str = None, compilation_unit: CompilationUnit = None, line: int = -1, column: int = -1, length: int = -1):
        self.name = name
        self.compilation_unit = compilation_unit
        self.line = line
        self.column = column
        self.length = length

    def __repr__(self):
        return '{}({i.name!r}, {i.compilation_unit!r}, {i.line!r}, {i.column!r}, {i.length!r})'.format(self.__class__.__name__, i=self)


class FunctionDefinition(CommandDefinition):
    pass


class MacroDefinition(CommandDefinition):
    pass
