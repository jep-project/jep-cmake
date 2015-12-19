import os

import pytest

from jep_cmake.model import MacroDefinition, FunctionDefinition
from jep_cmake.analysis import FileAnalyzer, MacroDefinition
from jep_cmake.model import FunctionDefinition, MacroDefinition


@pytest.fixture(scope="module", autouse=True)
def ch_resources_dir():
    localdir = os.path.dirname(__file__)
    os.chdir(os.path.join(localdir, 'resources'))


def test_analyzer_analyze_file():
    analyzer = FileAnalyzer()
    analyzer.analyze('command-def.cmake')

    assert_commands(analyzer)


def assert_commands(analyzer):
    assert len(analyzer.commands) == 4
    c = analyzer.commands[0]
    assert c.name == 'macro1'
    assert c.pos == 420
    assert c.length == 6
    c = analyzer.commands[1]
    assert c.name == 'macro2'
    assert c.pos == 611
    assert c.length == 6
    c = analyzer.commands[2]
    assert c.name == 'function1'
    assert c.pos == 654
    assert c.length == 9
    c = analyzer.commands[3]
    assert c.name == 'function2'
    assert c.pos == 692
    assert c.length == 9


def test_analyzer_analyze_buffer():
    analyzer = FileAnalyzer()
    analyzer.analyze('command-def.cmake', data="""
#######################################################################################################################
# Test file for command definitions in CMake
#######################################################################################################################
if(COMMAND_DEF_INCLUDED)
  return()
endif(COMMAND_DEF_INCLUDED)
set(COMMAND_DEF_INCLUDED true)

include(SomeModule)


macro(macroX)
    ZSG_CMAKE_PARSE_ARGUMENTS(arg "" "SOME_ARG;OTHER_ARG" "SOME_OPTION" ${ARGN})
    get_filename_component(absoluteTargetModelDirectory ${SOME_ARG} ABSOLUTE)
endmacro()

macro(macroY arg1 arg2)
endmacro()

function(functionA)
endfunction()

function(functionB arg1 arg2)
endfunction()
""")

    assert len(analyzer.commands) == 4
    assert analyzer.commands[0].name == 'macroX'
    assert analyzer.commands[1].name == 'macroY'
    assert analyzer.commands[2].name == 'functionA'
    assert analyzer.commands[3].name == 'functionB'

