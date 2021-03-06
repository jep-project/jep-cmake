/**
 * Simplified cmake grammar.
 *
 * Created from specification in https://cmake.org/cmake/help/v3.0/manual/cmake-language.7.html#syntax. Simplified to allow detection of command and variable definitions
 * supporting code completion via JEP.
 *
 * Missing: CMake 3+ support for new bracketed arguments and comments syntax.
 */
grammar cmake;

compilationUnit
    : fileElement*
    ;

fileElement
    : commandInvocation
    ;


commandInvocation
    : command=IDENTIFIER groupedArguments
    ;

groupedArguments
    : BRACKET_OPEN argument* BRACKET_CLOSE
    ;

argument
    : QUOTED_ARGUMENT
    | UNQUOTED_ARGUMENT
    | IDENTIFIER
    | groupedArguments
    ;

BRACKET_OPEN: '(';
BRACKET_CLOSE: ')';

IDENTIFIER
    : ('A'..'Z' | 'a'..'z' | '_') ('A'..'Z' | 'a'..'z' | '0'..'9' | '_')*
    ;

UNQUOTED_ARGUMENT
    : UNQUOTED_ELEMENT+
    ;

fragment UNQUOTED_ELEMENT
    : ~(' ' | '\t' | '\r' | '\n' | '(' | ')' | '#' | '"' | '\\')
    | ESCAPE_SEQUENCE
    ;

QUOTED_ARGUMENT
    : '"' QUOTED_ELEMENT* '"'
    ;

fragment QUOTED_ELEMENT
    : ~('\\' | '"' | '\r' | '\n')
    | ESCAPE_SEQUENCE
    | QUOTED_CONTINUATION
    ;

fragment QUOTED_CONTINUATION
    : '\\' LINEEND
    ;

fragment ESCAPE_SEQUENCE
    : ESCAPE_IDENTITY | ESCAPE_ENCODED | ESCAPE_SEMICOLON
    ;

fragment ESCAPE_IDENTITY
    : '\\(' | '\\)' | '\\#' | '\\"' | '\\ ' | '\\\\' | '\\$' | '\\@' | '\\^'
    ;

fragment ESCAPE_ENCODED
    : '\\t' | '\\r' | '\\n'
    ;

fragment ESCAPE_SEMICOLON
    : '\\;'
    ;

SKIP
    : (SPACES | LINEEND | COMMENT) -> skip
    ;

fragment LINEEND
    : '\r'? ('\n'|'\r'|EOF)
    ;

fragment SPACES
    : [ \t]+
    ;

fragment COMMENT
    : '#' ~[\n\r]* LINEEND
    ;
