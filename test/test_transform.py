import os

import pytest

from jep_cmake.ast import MacroDefinition, FunctionDefinition
from jep_cmake.transform import Transformer


@pytest.fixture(scope="module", autouse=True)
def ch_resources_dir():
    localdir = os.path.dirname(__file__)
    os.chdir(os.path.join(localdir, 'resources'))


def test_transformer_read_file():
    t = Transformer()
    compilation_unit = t.read('command-def.cmake')

    found_macro_names = {e.name for e in compilation_unit.fileelements if isinstance(e, MacroDefinition)}
    found_func_names = {e.name for e in compilation_unit.fileelements if isinstance(e, FunctionDefinition)}

    assert found_macro_names == {'macro1', 'macro2'}
    assert found_func_names == {'function1', 'function2'}

    c = t.command_table['macro1']
    assert c.line == 12
    assert c.column == 7
    assert c.length == 6

    c = t.command_table['macro2']
    assert c.line == 17
    assert c.column == 8
    assert c.length == 6

    c = t.command_table['function1']
    assert c.line == 20
    assert c.column == 10
    assert c.length == 9

    c = t.command_table['function2']
    assert c.line == 23
    assert c.column == 10
    assert c.length == 9


def test_transformer_read_buffer():
    t = Transformer()
    compilation_unit = t.read('command-def.cmake', data="""
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

    found_macro_names = {e.name for e in compilation_unit.fileelements if isinstance(e, MacroDefinition)}
    found_func_names = {e.name for e in compilation_unit.fileelements if isinstance(e, FunctionDefinition)}

    assert found_macro_names == {'macroX', 'macroY'}
    assert found_func_names == {'functionA', 'functionB'}
