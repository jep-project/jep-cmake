"""Knowledge about a CMake project and the file contained. Answers questions about CMake asked by frontend."""
import logging
import os

from jep_cmake.analysis import FileAnalyzer
from jep_cmake.model import CMakeFile

_logger = logging.getLogger(__name__)


class Project:
    def __init__(self, srcdir=None, *, file_analyzer=None):
        # TODO: if srcdir is None, look for .jep file
        self.srcdir = srcdir
        self.cmake_file_map = {}

        self._file_analyzer = file_analyzer or FileAnalyzer()

    def update(self, filepath, data=None):
        """Updates project after changes to file.

        :param filepath: Path to file that was changed.
        :param data: Optional content buffer. If given, this buffer is used instead of the actual file content.
        """

        cmake_file = self.cmake_file_map.get(filepath)
        if cmake_file is None:
            cmake_file = CMakeFile(filepath)
            self.cmake_file_map[filepath] = cmake_file

        self._file_analyzer.analyze(cmake_file, data)

    def completion_option_iter(self, filepath, pos):
        """Returns iterator over completion options."""

        # TODO: determine prefix from position
        # TODO: later, determine also command local scopes
        # TODO: later, determine type of allowed token

        # for now commands only, no prefix handling yet:
        cmake_file = self.cmake_file_map.get(filepath)
        if cmake_file and cmake_file.in_command_name_slot(pos):
            commands = cmake_file.commands
            origin, _ = os.path.splitext(os.path.basename(filepath))
            _logger.debug('Completion request in command slot, pos={}.'.format(pos))
            return ((command.name, origin) for command in commands)
        else:
            _logger.debug('Completion request outside of command slot, pos={}.'.format(pos))
            return []
