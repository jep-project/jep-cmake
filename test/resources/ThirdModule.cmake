# an included module with circular dependency

include(SomeModule)

function(func_from_third)
endfunction()
