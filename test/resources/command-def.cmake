#######################################################################################################################
# Test file for command definitions in CMake
#######################################################################################################################
if(COMMAND_DEF_INCLUDED)
  return()
endif(COMMAND_DEF_INCLUDED)
set(COMMAND_DEF_INCLUDED true)

include(SomeModule)
include("OtherModule.cmake")


macro(macro1)
    ZSG_CMAKE_PARSE_ARGUMENTS(arg "" "SOME_ARG;OTHER_ARG" "SOME_OPTION" ${ARGN})
    get_filename_component(absoluteTargetModelDirectory ${SOME_ARG} ABSOLUTE)
endmacro()

 macro(macro2 arg1 arg2)
 endmacro()

function(function1)
endfunction()

function(function2 arg1 arg2)
endfunction()

macro1()
macro2(A B)
function1()
function2(C D)


# functions and macros in comments and strings must not be found!

# function(functionBad1)
# endfunction()

set(var "\
function(functionBad2) \
endfunction() \
")
