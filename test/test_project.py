import os

import pytest

from jep_cmake.project import Project


@pytest.fixture(scope="module", autouse=True)
def ch_resources_dir():
    localdir = os.path.dirname(__file__)
    os.chdir(os.path.join(localdir, 'resources'))


def test_module_resolution():
    project = Project()
    cmake_filepath = os.path.abspath('command-def.cmake')
    project.update(cmake_filepath).result()
    cmake_file = project.cmake_file_by_path[cmake_filepath]

    assert len(cmake_file.includes) == 2
    assert len(cmake_file.resolved_includes) == 1

    included_cmake_filepath = os.path.abspath('SomeModule.cmake')
    assert cmake_file.resolved_includes[0] is project.cmake_file_by_path[included_cmake_filepath]
    project.shutdown_async_analysis()


def test_recursive_command_resolution():
    project = Project()
    cmake_filepath = os.path.abspath('command-def.cmake')
    included_cmake_filepath = os.path.abspath('SomeModule.cmake')
    third_cmake_filepath = os.path.abspath('ThirdModule.cmake')

    # force all files to be read completely:
    project.update(cmake_filepath).result()
    project.update(included_cmake_filepath).result()
    project.update(third_cmake_filepath).result()

    commands = set(project.command_iter(project.cmake_file_by_path[cmake_filepath]))

    # make sure all visible commands are available
    assert len(commands) == 6
    assert ('macro1', 'command-def') in commands
    assert ('macro2', 'command-def') in commands
    assert ('function1', 'command-def') in commands
    assert ('function2', 'command-def') in commands
    assert ('func_from_included', 'SomeModule') in commands
    assert ('func_from_third', 'ThirdModule') in commands
    project.shutdown_async_analysis()


def test_builtin_command_resolution_none():
    project = Project()
    cmake_filepath = os.path.abspath('command-def.cmake')
    project.update(cmake_filepath).result()
    commands = set(project.command_iter(project.cmake_file_by_path[cmake_filepath]))

    assert ('add_library', 'cmake') not in commands
    assert ('ctest_configure', 'ctest') not in commands
    assert ('exec_program', 'deprecated') not in commands
    project.shutdown_async_analysis()


def test_builtin_command_resolution_cmake():
    project = Project(builtin_commands=True)
    cmake_filepath = os.path.abspath('command-def.cmake')
    project.update(cmake_filepath).result()
    commands = set(project.command_iter(project.cmake_file_by_path[cmake_filepath]))

    assert ('add_library', 'cmake') in commands
    assert ('ctest_configure', 'ctest') not in commands
    assert ('exec_program', 'deprecated') not in commands
    project.shutdown_async_analysis()


def test_builtin_command_resolution_ctest():
    project = Project(ctest_commands=True)
    cmake_filepath = os.path.abspath('command-def.cmake')
    project.update(cmake_filepath).result()
    commands = set(project.command_iter(project.cmake_file_by_path[cmake_filepath]))

    assert ('add_library', 'cmake') not in commands
    assert ('ctest_configure', 'ctest') in commands
    assert ('exec_program', 'deprecated') not in commands
    project.shutdown_async_analysis()


def test_builtin_command_resolution_deprecated():
    project = Project(deprecated_commands=True)
    cmake_filepath = os.path.abspath('command-def.cmake')
    project.update(cmake_filepath).result()
    commands = set(project.command_iter(project.cmake_file_by_path[cmake_filepath]))

    assert ('add_library', 'cmake') not in commands
    assert ('ctest_configure', 'ctest') not in commands
    assert ('exec_program', 'deprecated') in commands
    project.shutdown_async_analysis()
