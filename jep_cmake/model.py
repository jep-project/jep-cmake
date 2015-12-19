"""CMake object model."""


class CMakeFile:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.commands = []

    def __repr__(self):
        return 'CMakeFile({!r})'.format(self.filepath)


class CommandDefinition:
    def __init__(self, name: str = None, line: int = -1, column: int = -1, length: int = -1):
        self.name = name
        self.line = line
        self.column = column
        self.length = length

    def __repr__(self):
        return '{}({i.name!r}, {i.line!r}, {i.column!r}, {i.length!r})'.format(self.__class__.__name__, i=self)


class FunctionDefinition(CommandDefinition):
    pass


class MacroDefinition(CommandDefinition):
    pass