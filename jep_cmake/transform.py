"""Transformation of parse tree to AST."""
import logging
import os

import antlr4
import antlr4.error.ErrorListener
import collections

from jep_cmake.ast import CompilationUnit, FunctionDefinition, MacroDefinition
from jep_cmake.parser.cmakeLexer import cmakeLexer
from jep_cmake.parser.cmakeListener import cmakeListener
from jep_cmake.parser.cmakeParser import cmakeParser

_logger = logging.getLogger(__name__)


class FileAnalyzer(cmakeListener, antlr4.error.ErrorListener.ErrorListener):
    """CMake analysis of a single file."""

    def __init__(self):
        #: Compilation unit AST element built during last transformation.
        self.compilation_unit = None

        #: Map of commands by name.
        self.command_table = {}

        #: Map of CMake built-in commands to handler functions.
        self._command_handler = collections.defaultdict(lambda: self.enter_unhandled_command,
                                                        function=self.enter_function,
                                                        macro=self.enter_macro)

        #: Current command being parsed.
        self._current_command = None

    def analyze(self, filepath, data=None) -> CompilationUnit:
        """Reads CMake file and builds AST from it.

        :param filepath: Path to CMake file to be processed.
        :param data: Optional string buffer to read unit from. If not given, the referenced file at ``filepath`` is read.
        :return: Top level ``CompilationUnit`` of read file.
        """

        self.compilation_unit = CompilationUnit(filepath)
        self.command_table.clear()
        self._current_command = None

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

        return self.compilation_unit

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        _logger.error('%s (%d:%d): %s' % (self.compilation_unit.filepath, line, column, msg))

    def enterCommandInvocation(self, ctx: cmakeParser.CommandInvocationContext):
        # cmake commands are case insensitive:
        command = ctx.command.text.lower()

        if self._current_command:
            _logger.warning('Unfinished command evaluation when starting {}.'.format(command))

        self._command_handler[command](ctx)

    def enter_unhandled_command(self, ctx):
        pass

    def enter_function(self, ctx):
        self._current_command = FunctionDefinition()

    def enter_macro(self, ctx):
        self._current_command = MacroDefinition()

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
            command.compilation_unit = self.compilation_unit
            self.compilation_unit.fileelements.append(command)

            _logger.debug('Found command definition {}.'.format(command))

            self.command_table[command.name] = command


class ProjectAnalyzer:
    """Analysis of a collection of files."""

    def __init__(self):
        #: File analyzer by filepath.
        self.file_analyzers = {}

    def analyze(self, filepath, data):
        """Analyzes given file with optional preread data buffer."""

        file_analyzer = self.file_analyzers.get(filepath)
        if not file_analyzer:
            _logger.debug('Setting up new analyzer for file {}.'.format(filepath))
            file_analyzer = FileAnalyzer()
            self.file_analyzers[filepath] = file_analyzer

        file_analyzer.analyze(filepath, data)

    def get_possible_commands(self, filepath, pos, prefix):
        """Returns commands visible in file at position, starting with given prefix."""

        # TODO: incomplete

        file_analyzer = self.file_analyzers.get(filepath)
        if file_analyzer:
            origin, _ = os.path.splitext(os.path.basename(file_analyzer.compilation_unit.filepath))
            return ((command, origin) for command in file_analyzer.command_table)
        else:
            _logger.debug('File {} unknown, cannot evaluate completion options.'.format(filepath))
            return tuple()


