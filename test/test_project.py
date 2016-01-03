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
