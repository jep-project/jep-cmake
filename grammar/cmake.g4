/**
 * Simplified cmake grammar.
 *
 * Created from specification in https://cmake.org/cmake/help/v3.0/manual/cmake-language.7.html#syntax. Simplified to allow detection of command and variable definitions
 * supporting code completion via JEP.
 *
 * Missing: CMake 3+ support for new bracketed and quoted argument syntax forms.
 */
grammar cmake;

compilation_unit
    : file_element*
    ;

file_element
    : WS+
    | LINE_COMMENT+
    | command_invocation
    ;


command_invocation
    : command=ID WS* '(' WS* (argument (WS+ argument)*)? WS* ')'
    ;

argument
    : STRING_LITERAL
    | INTEGER_LITERAL
    | .+?  // non-greedy, exit ASAP
    ;



STRING_LITERAL
    : '"' ( ESCAPE_SEQUENCE | ~('\\' | '"') )* '"'
    ;

INTEGER_LITERAL
    : ('0'..'9' '0'..'9'*)
    ;

ID
    : ID_FIRST_CHAR ID_NEXT_CHAR*
    ;

FILEPATH
    : DRIVE_LETTER? SLASH? (
          ('.' PATH_CHAR_NO_DOT PATH_CHAR*)
        | ('..' PATH_CHAR+)
        | (PATH_CHAR_NO_DOT PATH_CHAR*)
      )
    ;

LINE_COMMENT
    : '#' ~[\n\r']* '\r'? ('\n'|'\r'|EOF)
    ;

WS
    : [ \t\n\r]+
    ;

fragment ESCAPE_SEQUENCE
    : '\\' ('b' | 't' | 'n' | 'f' | 'r' | '\"' | '\'' | '\\')
    ;

fragment ID_FIRST_CHAR
    : ('a'..'z'|'A'..'Z'|'_')
    ;

fragment ID_NEXT_CHAR
    : (ID_FIRST_CHAR|'0'..'9')
    ;

fragment PATH_CHAR_NO_DOT
    : (ID_NEXT_CHAR|SLASH|'-')
    ;

fragment PATH_CHAR
    : (PATH_CHAR_NO_DOT|'.')
    ;

fragment SLASH
    : ('/'|'\\')
    ;

fragment DRIVE_LETTER
    : ('a'..'z'|'A'..'Z') ':'
    ;

