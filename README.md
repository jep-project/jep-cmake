# jep-cmake [![Build Status](https://travis-ci.org/jep-project/jep-cmake.svg)](https://travis-ci.org/jep-project/jep-cmake)

JEP-based CMake support in the making.

Once completed, this is a command line application implementing a JEP backend for CMake. It enables editors that have JEP-plugin installed to
improve their CMake editing support beyong pure syntax highlighting.

## Current state and features

* Parser for CMake files.
* Builds dictionary of user functions and macros.

## Upcoming features and feature ideas

* Code completion of commands (built-in and user functions and macros), first per currently edited file.
* Code completion for all files in a project, respecting CMake scope rules and module imports.
* Code completion for variables (respecting scope rules).
* Code completion for targets.
* Go to definition of commands, variables, targets.
* Error annotations.
* Renaming of user commands, variables, targets.

## Installation

From a Python 3.3+ environment install package from Github (will be uploaded to PyPI when more mature):

    > pip install https://github.com/jep-project/jep-cmake/archive/master.zip
    
After installation, the Python environment has a new command `jep-cmake`, that will run the backend.

## Usage

See the [JEP protocol|https://github.com/jep-project/jep/blob/master/protocol.md] for detailed instruction how to configure JEP via a
`.jep` file. In the most simple situation (`jep-cmake` in path, ...) the following `.jep` file in the root folder of your project that
contains CMake files should be enough:

    *.cmake,CMakeLists.txt:
    jep-cmake

Currently `jep-cmake` does not take any command line arguments.
