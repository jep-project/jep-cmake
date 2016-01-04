"""CMake object model."""
import bisect


class CMakeFile:
    def __init__(self, filepath: str):
        self.filepath = filepath
        #: List of commands defined in this file.
        self.command_definitions = []
        #: List of CMake modules loaded via include statements (without '.cmake' extension).
        self.includes = []

        #: Offsets into file's character stream, where command names begin to be possible and where not.
        self.command_name_slots = []

        #: Resolved references to included modules.
        self.resolved_includes = []

    def movefrom(self, other):
        """Move content of other CMake file into this one."""

        self.filepath = other.filepath
        self.command_definitions = other.command_definitions
        self.includes = other.includes
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
    def __init__(self, arg0: str = None, pos: int = -1, length: int = -1):
        #: First argument of command invocation.
        self.arg0 = arg0
        self.pos = pos
        self.length = length

    def __repr__(self):
        return '{}({i.arg0!r}, {i.pos!r}, {i.length!r})'.format(self.__class__.__name__, i=self)


class CommandDefinition(CommandInvocation):
    @property
    def name(self):
        return self.arg0


class FunctionDefinition(CommandDefinition):
    pass


class MacroDefinition(CommandDefinition):
    pass


class ModuleInclude(CommandInvocation):
    @property
    def modulename(self):
        return self.arg0
