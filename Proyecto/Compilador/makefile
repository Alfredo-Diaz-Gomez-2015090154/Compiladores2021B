compilacion: grammar.y lexer.l symbolTable.c
	bison -d -v grammar.y
	flex lexer.l
	gcc -c grammar.tab.c
	gcc -c lex.yy.c
	gcc -c symbolTable.c
	gcc -c attribute.c
	gcc lex.yy.o grammar.tab.o symbolTable.o attribute.o -lfl -lm