compilacion: mfcalc.y mfcalc.l tablaSimbolos.c
	bison -d mfcalc.y
	flex mfcalc.l
	gcc -c mfcalc.tab.c
	gcc -c lex.yy.c
	gcc -c tablaSimbolos.c
	gcc -c funcionesPropias.c
	gcc lex.yy.o mfcalc.tab.o tablaSimbolos.o  funcionesPropias.o -lfl -lm