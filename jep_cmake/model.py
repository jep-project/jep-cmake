"""CMake object model."""
import bisect
import collections


class CMakeFile:
    def __init__(self, filepath: str):
        self.filepath = filepath
        #: List of command names defined in this file.
        self.commands = []
        #: List of CMake modules loaded via import statements (without '.cmake' extension).
        self.imports = []

        #: Offsets into file's character stream, where command names begin to be possible and where not.
        self.command_name_slots = []

    def movefrom(self, other):
        """Move content of other CMake file into this one."""

        self.filepath = other.filepath
        self.commands = other.commands
        self.imports = other.imports
        self.command_name_slots = other.command_name_slots

        other.clear()

    def clear(self):
        self.__init__(self.filepath)

    def prohibit_command_name(self, start, end):
        self.command_name_slots.append(start)
        self.command_name_slots.append(end)

    def __repr__(self):
        return 'CMakeFile({!r})'.format(self.filepath)

    def in_command_name_slot(self, pos):
        """Returns flag if given character position is valid for command names."""
        return bisect.bisect_right(self.command_name_slots, pos) & 1 == 0


class CommandInvocation:
    def __init__(self, name: str = None, pos: int = -1, length: int = -1):
        self.name = pos
        self.length = length

    def __repr__(self):
        return '{}({i.name!r}, {i.pos!r}, {i.length!r})'.format(self.__class__.__name__, i=self)


class CommandDefinition(CommandInvocation):
    pass


class FunctionDefinition(CommandDefinition):
    pass


class MacroDefinition(CommandDefinition):
    pass


class ModuleInclude(CommandInvocation):
    pass
