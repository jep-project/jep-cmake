import os

import pytest

from jep_cmake.model import CMakeFile
from jep_cmake.analysis import FileAnalyzer


@pytest.fixture(scope="module", autouse=True)
def ch_resources_dir():
    localdir = os.path.dirname(__file__)
    os.chdir(os.path.join(localdir, 'resources'))


def test_analyzer_analyze_file():
    cmake_file = CMakeFile('command-def.cmake')
    analyzer = FileAnalyzer()

    assert not analyzer.running
    analyzer.analyze(cmake_file)
    assert not analyzer.running

    assert len(cmake_file.command_definitions) == 4
    c = cmake_file.command_definitions[0]
    assert c.name == 'macro1'
    assert c.pos == 438
    assert c.length == 6
    c = cmake_file.command_definitions[1]
    assert c.name == 'macro2'
    assert c.pos == 624
    assert c.length == 6
    c = cmake_file.command_definitions[2]
    assert c.name == 'function1'
    assert c.pos == 664
    assert c.length == 9
    c = cmake_file.command_definitions[3]
    assert c.name == 'function2'
    assert c.pos == 699
    assert c.length == 9

    assert len(cmake_file.includes) == 2
    assert cmake_file.includes[0].modulename == 'SomeModule'
    assert cmake_file.includes[1].modulename == 'OtherModule.cmake'


def test_analyzer_analyze_buffer():
    cmake_file = CMakeFile('command-def.cmake')
    analyzer = FileAnalyzer()
    analyzer.analyze(cmake_file, data="""
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

    assert len(cmake_file.command_definitions) == 4
    assert cmake_file.command_definitions[0].name == 'macroX'
    assert cmake_file.command_definitions[1].name == 'macroY'
    assert cmake_file.command_definitions[2].name == 'functionA'
    assert cmake_file.command_definitions[3].name == 'functionB'


def test_async_analysis():
    cmf = CMakeFile('command-def.cmake')
    analyzer = FileAnalyzer()

    assert not analyzer.running
    f = analyzer.analyze_async(cmf)
    assert analyzer.running
    cmake_file = f.result()
    assert not analyzer.running

    assert len(cmake_file.command_definitions) == 4
    assert cmake_file.command_definitions[0].name == 'macro1'
    assert cmake_file.command_definitions[1].name == 'macro2'
    assert cmake_file.command_definitions[2].name == 'function1'
    assert cmake_file.command_definitions[3].name == 'function2'

def test_cp1252_decoding():
    cmf = CMakeFile('CP1252Module.cmake')
    analyzer = FileAnalyzer()
    f = analyzer.analyze_async(cmf)
    cmake_file = f.result()
    assert cmake_file
