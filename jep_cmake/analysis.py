"""Analysis of a single CMake file through parser invocation."""
import collections
import logging
import timeit
from concurrent import futures

import antlr4
import antlr4.error.ErrorListener
import chardet

from jep_py.content import NewlineMode
from jep_cmake.model import FunctionDefinition, MacroDefinition, ModuleInclude
from jep_cmake.parser.cmakeLexer import cmakeLexer
from jep_cmake.parser.cmakeListener import cmakeListener
from jep_cmake.parser.cmakeParser import cmakeParser

_logger = logging.getLogger(__name__)


class FileAnalyzer(cmakeListener, antlr4.error.ErrorListener.ErrorListener):
    """CMake analysis of a single file."""

    #: Executor to run CPU-bound analysis in separate process. Important to be defined at class level to allow pickling ``self``.
    _async_executor = None

    def __init__(self):
        #: CMake file currently being analyzed.
        self._cmake_file = None
        #: Cache for tree walker, last found command.
        self._current_command = None
        #: Cache for tree walker, collection in CMake container to add last processed command to.
        self._current_command_list = None

    @property
    def running(self):
        """Flag whether this analyzer is currently analyzing a file."""
        return self._cmake_file is not None

    def clear(self):
        self.__init__()

    def analyze(self, cmake_file, data=None, newline_mode=NewlineMode.Unknown):
        """Reads CMake file and builds AST from it.

        :param cmake_file: Container to hold found information.
        :param data: Optional string buffer to read unit from. If not given, the referenced file at ``filepath`` is read.
        :param newline_mode: Newline mode (of frontend) to be matched when reading files from disk to get correct character indexes.
        :return: Reference to filled CMake file container (same as was passed in).
        """

        self.clear()
        self._cmake_file = cmake_file
        cmake_file.clear()

        if not data:
            # read data buffer first to use newline translation:
            _logger.debug('Parsing file {}.'.format(cmake_file.filepath))
            open_newline_mode = NewlineMode.open_newline_mode(newline_mode)

            try:
                data = self._readfile(cmake_file, 'utf-8', open_newline_mode)
            except UnicodeDecodeError:
                _logger.debug('Triggering encoding detection of {}.'.format(cmake_file.filepath))

                with open(cmake_file.filepath, 'rb') as f:
                    data = f.read()
                    result = chardet.detect(data)
                    enc = result['encoding']
                    conf = result['confidence']
                    _logger.debug('Detected file encoding {} with confidence {:.2f}.'.format(enc, conf))

                data = self._readfile(cmake_file, enc, open_newline_mode)

        else:
            _logger.debug('Parsing data buffer for {}.'.format(cmake_file.filepath))

        stream = antlr4.InputStream(data)
        lexer = cmakeLexer(stream)
        tstream = antlr4.CommonTokenStream(lexer)
        parser = cmakeParser(tstream)
        parser.addErrorListener(self)
        tree = parser.compilationUnit()
        _logger.debug('Parse tree complete.')

        walker = antlr4.ParseTreeWalker()
        walker.walk(self, tree)
        _logger.debug('AST complete.')

        self._cmake_file = None

        return cmake_file

    @classmethod
    def _readfile(cls, cmake_file, encoding, open_newline_mode):
        with open(cmake_file.filepath, encoding=encoding, newline=open_newline_mode) as f:
            return f.read()

    @classmethod
    def get_async_executor(cls):
        if not cls._async_executor:
            cls._async_executor = futures.ProcessPoolExecutor()
        return cls._async_executor

    @classmethod
    def shutdown_async_executor(cls, wait=True):
        """Shuts down the executor cleanly."""
        if cls._async_executor:
            executor = cls._async_executor
            cls._async_executor = None
            executor.shutdown(wait)

    def analyze_async(self, cmake_file, data=None, newline_mode=NewlineMode.Unknown):
        """Calls ``analyze`` asynchronously.

        :param cmake_file: Container to hold found information.
        :param data: Optional string buffer to read unit from. If not given, the referenced file at ``filepath`` is read.
        :param newline_mode: Newline mode (of frontend) to be matched when reading files from disk to get correct character indexes.
        :return: Future to resulting CMake file container.
        """
        self._cmake_file = cmake_file
        start = timeit.default_timer()

        def future_done(f):
            self._cmake_file = None
            end = timeit.default_timer()
            _logger.debug('Took {:.3f}s to asynchronously analyze {}.'.format(end - start, cmake_file.filepath))

        future = self.get_async_executor().submit(self.analyze, cmake_file, data)
        future.add_done_callback(future_done)

        return future

    def enter_unhandled_command(self, ctx):
        pass

    def enter_function(self, ctx):
        self._current_command = FunctionDefinition()
        self._current_command_list = self._cmake_file.command_definitions

    def enter_macro(self, ctx):
        self._current_command = MacroDefinition()
        self._current_command_list = self._cmake_file.command_definitions

    def enter_include(self, ctx):
        self._current_command = ModuleInclude()
        self._current_command_list = self._cmake_file.includes

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        _logger.error('%s (%d:%d): %s' % (self._cmake_file.filepath, line, column, msg))

    COMMAND_HANDLER = collections.defaultdict(lambda: FileAnalyzer.enter_unhandled_command)
    COMMAND_HANDLER.update({
        'function': enter_function,
        'macro': enter_macro,
        'include': enter_include
    })

    def enterCommandInvocation(self, ctx: cmakeParser.CommandInvocationContext):
        # cmake commands are case insensitive:
        command = ctx.command.text.lower()

        if self._current_command:
            _logger.warning('Unfinished command evaluation when starting {}.'.format(command))

        self.COMMAND_HANDLER[command](self, ctx)

        # no command names after opening bracket and before closing bracket:
        self._cmake_file.prohibit_command_name(ctx.children[1].start.start + 1, ctx.stop.stop + 1)

    def enterArgument(self, ctx: cmakeParser.ArgumentContext):
        # for now only record first argument of command definitions:
        if self._current_command:
            command = self._current_command
            self._current_command = None

            # get the token that was used for this argument:
            quoted = False
            token = ctx.IDENTIFIER()
            if not token:
                token = ctx.UNQUOTED_ARGUMENT()
            if not token:
                quoted = True
                token = ctx.QUOTED_ARGUMENT()
            if not token:
                # other forms (e.g. grouped) not handled at this level, dive down:
                return

            symbol = token.symbol
            command.arg0 = symbol.text if not quoted else symbol.text[1:-1]
            command.pos = symbol.start
            command.length = 1 + symbol.stop - symbol.start

            self._current_command_list.append(command)
            self._current_command_list = None
