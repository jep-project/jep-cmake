from unittest import mock

from jep_cmake.model import CMakeFile


def test_cmake_file_in_command_name_slot():
    cmake_file = CMakeFile(mock.sentinel.FILENAME)
    cmake_file.append_command_name_slot(10, 20)
    cmake_file.append_command_name_slot(30, 40)

    assert not cmake_file.in_command_name_slot(0)
    assert not cmake_file.in_command_name_slot(9)

    assert cmake_file.in_command_name_slot(10)
    assert cmake_file.in_command_name_slot(11)
    assert cmake_file.in_command_name_slot(19)

    assert not cmake_file.in_command_name_slot(20)
    assert not cmake_file.in_command_name_slot(21)
    assert not cmake_file.in_command_name_slot(29)

    assert cmake_file.in_command_name_slot(30)
    assert cmake_file.in_command_name_slot(31)
    assert cmake_file.in_command_name_slot(39)

    assert not cmake_file.in_command_name_slot(40)
    assert not cmake_file.in_command_name_slot(41)
