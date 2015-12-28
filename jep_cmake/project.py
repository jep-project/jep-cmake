"""Knowledge about a CMake project and the file contained. Answers questions about CMake asked by frontend."""
import fnmatch
import logging
import os

import itertools
import timeit

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
        self._cmake_file_map = {}
        self._file_analyzer_map = {}

        # lookup by module name:
        self._module_by_name = {}

    def update(self, filepath, data=None):
        """Updates project after changes to file.

        :param filepath: Path to file that was changed.
        :param data: Optional content buffer. If given, this buffer is used instead of the actual file content.
        """

        firsttime = len(self._cmake_file_map) == 0

        cmake_file = self._get_cmake_file(filepath)
        analyzer = self._file_analyzer_map[filepath]
        cmake_file_future = analyzer.analyze_async(cmake_file, data)
        cmake_file_future.add_done_callback(self.on_cmap_file_analysis_done)

        if firsttime:
            self.load_cmake_srcdir()

    def _get_cmake_file(self, filepath):
        cmake_file = self._cmake_file_map.get(filepath)
        if cmake_file is None:
            cmake_file = CMakeFile(filepath)
            self._cmake_file_map[filepath] = cmake_file
            self._file_analyzer_map[filepath] = self.file_analyzer_factory()

            # remember CMake modules:
            if fnmatch.fnmatch(filepath, CMAKE_MODULEFILE_PATTERN):
                pathnoext, _ = os.path.splitext(filepath)
                modulename = os.path.basename(pathnoext)
                self._module_by_name[modulename] = cmake_file

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
        if cmake_file:
            if cmake_file.in_command_name_slot(pos):
                _logger.debug('Completion request in command slot, pos={}.'.format(pos))
                yield from self.command_iter(cmake_file)
                for visible_cmake_file in self.get_preloaded_cmake_files(cmake_file):
                    yield from self.command_iter(visible_cmake_file)
            else:
                _logger.debug('Completion request outside of command slot, pos={}.'.format(pos))
        else:
            _logger.debug('Cannot return code completion options for unknown file {}.'.format(filepath))

    def command_iter(self, cmake_file):
        commands = cmake_file.commands
        origin, _ = os.path.splitext(os.path.basename(cmake_file.filepath))
        return ((command.name, origin) for command in commands)

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

    def get_preloaded_cmake_files(self, cmake_file):
        """Returns list of CMake files whose contents are visible to given file."""
        # TODO: evaluate imports and hierarchy, depending on file extension.

        # dummy, just return all known modules:
        return self._module_by_name.values()
