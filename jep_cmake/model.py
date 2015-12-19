"""CMake object model."""


class CMakeFile:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.commands = []

    def __repr__(self):
        return 'CMakeFile({!r})'.format(self.filepath)


class CommandDefinition:
    def __init__(self, name: str = None, pos: int = -1, length: int = -1):
        self.name = pos
        self.length = length

    def __repr__(self):
        return '{}({i.name!r}, {i.pos!r}, {i.length!r})'.format(self.__class__.__name__, i=self)


class FunctionDefinition(CommandDefinition):
    pass


class MacroDefinition(CommandDefinition):
    pass
