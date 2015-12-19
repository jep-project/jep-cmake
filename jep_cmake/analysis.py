"""Analysis of a single CMake file through parser invocation."""
import collections
import logging

import antlr4
import antlr4.error.ErrorListener

from jep_cmake.model import FunctionDefinition, MacroDefinition
from jep_cmake.parser.cmakeLexer import cmakeLexer
from jep_cmake.parser.cmakeListener import cmakeListener
from jep_cmake.parser.cmakeParser import cmakeParser

_logger = logging.getLogger(__name__)


class FileAnalyzer(cmakeListener, antlr4.error.ErrorListener.ErrorListener):
    """CMake analysis of a single file."""

    def __init__(self):
        self.filepath = None
        self.commands = []
        self.targets = []
        self.variables = []

        #: Current command being parsed.
        self._current_command = None

    def clear(self):
        self.__init__()

    def analyze(self, filepath, data=None):
        """Reads CMake file and builds AST from it.

        :param filepath: Path to CMake file to be processed.
        :param data: Optional string buffer to read unit from. If not given, the referenced file at ``filepath`` is read.
        :return: Top level ``CompilationUnit`` of read file.
        """

        self.clear()
        self.filepath = filepath

        if data:
            _logger.debug('Parsing data buffer for {}.'.format(filepath))
            stream = antlr4.InputStream(data)
        else:
            _logger.debug('Parsing file {}.'.format(filepath))
            stream = antlr4.FileStream(filepath, encoding='utf-8')

        lexer = cmakeLexer(stream)
        tstream = antlr4.CommonTokenStream(lexer)
        parser = cmakeParser(tstream)
        parser.addErrorListener(self)
        tree = parser.compilationUnit()
        _logger.debug('Parse tree complete.')

        walker = antlr4.ParseTreeWalker()
        walker.walk(self, tree)
        _logger.debug('AST complete.')

    def enter_unhandled_command(self, ctx):
        pass

    def enter_function(self, ctx):
        self._current_command = FunctionDefinition()

    def enter_macro(self, ctx):
        self._current_command = MacroDefinition()

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        _logger.error('%s (%d:%d): %s' % (self.filepath, line, column, msg))

    COMMAND_HANDLER = collections.defaultdict(lambda: FileAnalyzer.enter_unhandled_command,
                                              function=enter_function,
                                              macro=enter_macro)

    def enterCommandInvocation(self, ctx: cmakeParser.CommandInvocationContext):
        # cmake commands are case insensitive:
        command = ctx.command.text.lower()

        if self._current_command:
            _logger.warning('Unfinished command evaluation when starting {}.'.format(command))

        self.COMMAND_HANDLER[command](self, ctx)

    def enterArgument(self, ctx: cmakeParser.ArgumentContext):
        # for now only record first argument of command definitions:
        if self._current_command:
            command = self._current_command
            self._current_command = None

            token = ctx.IDENTIFIER().symbol
            command.name = token.text
            command.line = token.line
            command.column = 1 + token.column
            command.length = 1 + token.stop - token.start

            _logger.debug('Found command definition {}.'.format(command))
            self.commands.append(command)

