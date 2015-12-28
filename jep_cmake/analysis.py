"""Analysis of a single CMake file through parser invocation."""
import collections
import logging
import timeit
from concurrent import futures

import antlr4
import antlr4.error.ErrorListener

from jep_cmake.model import FunctionDefinition, MacroDefinition
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

    @property
    def running(self):
        """Flag whether this analyzer is currently analyzing a file."""
        return self._cmake_file is not None

    def clear(self):
        self.__init__()

    def analyze(self, cmake_file, data=None):
        """Reads CMake file and builds AST from it.

        :param cmake_file: Container to hold found information.
        :param data: Optional string buffer to read unit from. If not given, the referenced file at ``filepath`` is read.
        :return: Reference to filled CMake file container (same as was passed in).
        """

        self.clear()
        self._cmake_file = cmake_file
        cmake_file.clear()

        if data:
            _logger.debug('Parsing data buffer for {}.'.format(cmake_file.filepath))
            stream = antlr4.InputStream(data)
        else:
            _logger.debug('Parsing file {}.'.format(cmake_file.filepath))
            stream = antlr4.FileStream(cmake_file.filepath, encoding='utf-8')

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
    def get_async_executor(cls):
        if not cls._async_executor:
            cls._async_executor = futures.ProcessPoolExecutor()
        return cls._async_executor

    def analyze_async(self, cmake_file, data=None):
        """Calls ``analyze`` asynchronously.

        :param cmake_file: Container to hold found information.
        :param data: Optional string buffer to read unit from. If not given, the referenced file at ``filepath`` is read.
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

    def enter_macro(self, ctx):
        self._current_command = MacroDefinition()

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        _logger.error('%s (%d:%d): %s' % (self._cmake_file.filepath, line, column, msg))

    COMMAND_HANDLER = collections.defaultdict(lambda: FileAnalyzer.enter_unhandled_command,
                                              function=enter_function,
                                              macro=enter_macro)

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

            token = ctx.IDENTIFIER().symbol
            command.name = token.text
            command.pos = token.start
            command.length = 1 + token.stop - token.start

            _logger.debug('Found command definition {}.'.format(command))
            self._cmake_file.commands.append(command)
