grammar conditions;

/*
 * Parser Rules
 */

conditions
	: '.'
	| condition '.'
	| condition ',' conditions
	;

condition
	: expression relation expression
	;

expression
	: operand
	| operand OPERATOR expression
	;

relation
	: EQ
	| LT
	| GT
	| LE
	| GE
	| NE
	;

operand
	: NUMBER
	| VARIABLE
	| '#' CHARACTER
	;

/*
 * Lexer Rules
 */

EQ
	: '=='
	;

LT
	: '<'
	;

GT
	: '>'
	;

LE
	: '<='
	;

GE
	: '>='
	;

NE
	: '!='
	;

OPERATOR
	: '+'
	| '-'
	| '*'
	| '/'
	| '%'
	;

NUMBER
	: [0-9]+
	;

VARIABLE
	: [A-Z]
	;

CHARACTER
	: [a-z]
	;