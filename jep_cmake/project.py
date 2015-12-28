"""Knowledge about a CMake project and the file contained. Answers questions about CMake asked by frontend."""
import logging
import os

from jep_cmake.analysis import FileAnalyzer
from jep_cmake.model import CMakeFile

_logger = logging.getLogger(__name__)


class Project:
    def __init__(self, srcdir=None, *, file_analyzer_factory=None):
        # TODO: if srcdir is None, look for .jep file
        self.srcdir = srcdir
        self.file_analyzer_factory = file_analyzer_factory or FileAnalyzer

        # lookups by filepath:
        self._cmake_file_map = {}
        self._file_analyzer_map = {}

    def update(self, filepath, data=None):
        """Updates project after changes to file.

        :param filepath: Path to file that was changed.
        :param data: Optional content buffer. If given, this buffer is used instead of the actual file content.
        """

        cmake_file = self._get_cmake_file(filepath)
        analyzer = self._file_analyzer_map[filepath]
        cmake_file_future = analyzer.analyze_async(cmake_file, data)
        cmake_file_future.add_done_callback(self.on_cmap_file_analysis_done)

    def _get_cmake_file(self, filepath):
        cmake_file = self._cmake_file_map.get(filepath)
        if cmake_file is None:
            cmake_file = CMakeFile(filepath)
            self._cmake_file_map[filepath] = cmake_file
            self._file_analyzer_map[filepath] = self.file_analyzer_factory()
        return cmake_file

    def on_cmap_file_analysis_done(self, cmake_file_future):
        cmake_file_parsed = cmake_file_future.result()
        cmake_file = self._get_cmake_file(cmake_file_parsed.filepath)
        cmake_file.copy(cmake_file_parsed)

    def completion_option_iter(self, filepath, pos):
        """Returns iterator over completion options."""

        # TODO: determine prefix from position
        # TODO: later, determine also command local scopes
        # TODO: later, determine type of allowed token

        # for now commands only, no prefix handling yet:
        cmake_file = self._cmake_file_map.get(filepath)
        if cmake_file and cmake_file.in_command_name_slot(pos):
            commands = cmake_file.commands
            origin, _ = os.path.splitext(os.path.basename(filepath))
            _logger.debug('Completion request in command slot, pos={}.'.format(pos))
            return ((command.name, origin) for command in commands)
        else:
            _logger.debug('Completion request outside of command slot, pos={}.'.format(pos))
            return []
