"""Knowledge about a CMake project and the file contained. Answers questions about CMake asked by frontend."""
import fnmatch
import logging
import os

import itertools
import timeit

import collections

from jep.content import NewlineMode
from jep_cmake.analysis import FileAnalyzer
from jep_cmake.model import CMakeFile

_logger = logging.getLogger(__name__)

CMAKE_MODULEFILE_PATTERN = '*.cmake'
CMAKE_LISTFILE_NAME = 'CMakeLists.txt'


class Project:
    def __init__(self, srcdir=None, *, file_analyzer_factory=None):
        #: CMake source directory of project.
        self.srcdir = srcdir or os.path.abspath('.')
        #: Factory function for cmake file parser.
        self.file_analyzer_factory = file_analyzer_factory or FileAnalyzer

        # lookups by filepath:
        self.cmake_file_by_path = {}
        self._analyzer_by_path = {}

        # lookup by module name:
        self._module_by_name = collections.defaultdict(lambda: None)

        #: detected newline encoding of frontend:
        self._newline_mode = NewlineMode.Unknown

    def update(self, filepath, data=None):
        """Updates project after changes to file.

        :param filepath: Path to file that was changed.
        :param data: Optional content buffer. If given, this buffer is used instead of the actual file content.
        :return: Future to parsed CMake file (mainly for testing).
        """

        firsttime = len(self.cmake_file_by_path) == 0

        # try to guess newline encoding from data provided by frontend:
        if self._newline_mode == NewlineMode.Unknown and data:
            self._newline_mode = NewlineMode.detect(data)
            _logger.debug('Detected newline mode 0x{:02x} from frontend.'.format(self._newline_mode))

        cmake_file = self._get_cmake_file(filepath)
        analyzer = self._analyzer_by_path[filepath]
        cmake_file_future = analyzer.analyze_async(cmake_file, data, self._newline_mode)
        cmake_file_future.add_done_callback(self.on_cmap_file_analysis_done)

        if firsttime:
            self.load_cmake_srcdir()

        return cmake_file_future

    def _get_cmake_file(self, filepath):
        cmake_file = self.cmake_file_by_path.get(filepath)
        if cmake_file is None:
            cmake_file = CMakeFile(filepath)
            self.cmake_file_by_path[filepath] = cmake_file
            self._analyzer_by_path[filepath] = self.file_analyzer_factory()

            # remember CMake modules:
            if fnmatch.fnmatch(filepath, CMAKE_MODULEFILE_PATTERN):
                pathnoext, _ = os.path.splitext(filepath)
                modulename = os.path.basename(pathnoext)
                self._module_by_name[modulename] = cmake_file

        return cmake_file

    def on_cmap_file_analysis_done(self, cmake_file_future):
        cmake_file_parsed = cmake_file_future.result()
        cmake_file = self._get_cmake_file(cmake_file_parsed.filepath)
        cmake_file.movefrom(cmake_file_parsed)

        # complete cmake file with project level data:
        cmake_file.resolved_includes = list(filter(None, (self._module_by_name[include.modulename] for include in cmake_file.includes)))

    def completion_option_iter(self, filepath, pos):
        """Returns iterator over completion options."""

        # TODO: determine prefix from position
        # TODO: later, determine also command local scopes
        # TODO: later, determine type of allowed token

        # for now commands only, no prefix handling yet:
        cmake_file = self.cmake_file_by_path.get(filepath)
        if cmake_file:
            _logger.debug('Command slot: {!r}.'.format(cmake_file.command_name_slots))
            if cmake_file.in_command_name_slot(pos):
                _logger.debug('Completion request in command slot, pos={}.'.format(pos))
                yield from self.command_iter(cmake_file)
                for included_cmake_file in cmake_file.resolved_includes:
                    yield from self.command_iter(included_cmake_file)
            else:
                _logger.debug('Completion request outside of command slot, pos={}.'.format(pos))
        else:
            _logger.debug('Cannot return code completion options for unknown file {}.'.format(filepath))

    def command_iter(self, cmake_file):
        visited_filepaths = set()
        return self._command_iter(cmake_file, visited_filepaths)

    def _command_iter(self, cmake_file, visited_filepaths):
        # first return the commands of this cmake file:
        visited_filepaths.add(cmake_file.filepath)
        origin, _ = os.path.splitext(os.path.basename(cmake_file.filepath))
        for command in cmake_file.command_definitions:
            yield (command.name, origin)

        # now return commands from included modules (recursively):
        for included_cmake_file in cmake_file.resolved_includes:
            # prevent following circular dependencies:
            if included_cmake_file.filepath not in visited_filepaths:
                yield from self._command_iter(included_cmake_file, visited_filepaths)

    def load_cmake_srcdir(self):
        _logger.debug('Starting to read complete project tree.')
        count = 0
        start = timeit.default_timer()

        for dirpath, dirnames, filenames in os.walk(self.srcdir):
            modules = fnmatch.filter(filenames, CMAKE_MODULEFILE_PATTERN)
            listfiles = fnmatch.filter(filenames, CMAKE_LISTFILE_NAME)

            filepaths = (os.path.join(dirpath, filename) for filename in itertools.chain(modules, listfiles))

            for path in filepaths:
                self.update(path)
                count += 1

        stop = timeit.default_timer()
        _logger.info('Triggered analysis of {} CMake files in {:.3f} seconds.'.format(count, stop - start))
        _logger.info('Found {} CMake modules.'.format(len(self._module_by_name)))
