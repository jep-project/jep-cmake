"""CMake object model."""
import bisect
import collections


class CMakeFile:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.commands = []

        # start and end in character stream where command names can be inserted, separated to allow using bisect without explicit key array:
        self._command_name_starts = []
        self._command_name_ends = []

    def clear(self):
        self.__init__(self.filepath)

    def append_command_name_slot(self, start, end):
        self._command_name_starts.append(start)
        self._command_name_ends.append(end)

    def __repr__(self):
        return 'CMakeFile({!r})'.format(self.filepath)

    def in_command_name_slot(self, pos):
        """Returns flag if given character position is part of a command name slot."""
        slot_index = bisect.bisect_right(self._command_name_starts, pos) - 1
        if slot_index >= 0:
            return self._command_name_starts[slot_index] <= pos < self._command_name_ends[slot_index]
        else:
            return False


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
