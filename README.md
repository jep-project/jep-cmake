# jep-cmake [![Build Status](https://travis-ci.org/jep-project/jep-cmake.svg)](https://travis-ci.org/jep-project/jep-cmake)

JEP-based CMake support in the making.

Once completed, this is a command line application implementing a JEP backend for CMake. It enables editors that have JEP-plugin installed to
improve their CMake editing support beyong pure syntax highlighting.

## Current state and features

* Parser for CMake files.
* Builds dictionary of user functions and macros.
* Code completion of commands (built-in and user functions and macros), from local and (directly or indirectly) imported modules.

## Upcoming features and feature ideas

* Code completion for all files in a project, including parent CMake files.
* Code completion for variables (respecting scope rules).
* Code completion for targets.
* Go to definition of commands, variables, targets.
* Error annotations.
* Renaming of user commands, variables, targets.

## Installation

Since the tool and associated libraries are under development, installation is only partly available via PyPI packages. In the meantime
follow this script to install the `jep-cmake` in you local Python (or virtual) environment:

    > git clone https://github.com/jep-project/jep-cmake.git
    > cd jep-cmake
    > pip install -r requirements.txt
    > pip install .
    
After installation, the Python environment has a new command `jep-cmake`, that will run the backend.

## Usage

See the [JEP protocol](https://github.com/jep-project/jep/blob/master/protocol.md) for detailed instruction how to configure JEP via a
`.jep` file. In the most simple situation (`jep-cmake` in path, ...) the following `.jep` file in the root folder of your project that
contains CMake files should be enough:

    *.cmake,CMakeLists.txt:
    jep-cmake

See `jep-cmake -h` for available command line options:

    > jep-cmake -h
    usage: jep-cmake-script.py [-h] [--version {2.8.12,3.4}] [--builtin-cmake]
                               [--builtin-ctest] [--builtin-deprecated]
    
    JEP backend providing CMake editing support.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version {2.8.12,3.4}
                            CMake version to be supported, mainly used for
                            completion of built-in commands.
      --builtin-cmake       If specified, built-in CMake commands are part of code
                            completion.
      --builtin-ctest       If specified, built-in ctest commands are part of code
                            completion.
      --builtin-deprecated  If specified, built-in CMake commands that have been
                            deprecated are part of code completion.

The various built-in options are available to finetune the backend's interaction with the editor being used. Some editors already support code completion for built-in
CMake commands. In that case it is more efficient remove them from the backends completion options (by not specifying the corresponding command line option). 
