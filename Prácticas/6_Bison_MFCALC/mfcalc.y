%{
#include <stdio.h>
#include "tablaSimbolos.h"
#include "funcionesPropias.h"
#include <math.h>

void yyerror(char *mensaje){
    printf("Error: %s", mensaje);
}

%}

%define api.value.type union
%token <double>  NUM
%token <symrec*> VAR FUN
%nterm <double>  exp

%precedence '='
%left '-' '+'
%left '*' '/'
%precedence NEG
%right '^'

%%
/* Definición de la gramática. */
entrada:
    %empty
|   entrada linea
;

linea:
    '\n'
|   exp '\n'            { printf("%.10g\n", $1); }
|   error '\n'          { yyerror; }
;

exp:
    NUM
|   VAR                 { $$ = $1->value.var; }
|   VAR '=' exp         { $$ = $3; $1->value.var = $3; }
|   FUN '(' exp ')'     { $$ = $1->value.fun($3); }
|   exp '+' exp         { $$ = $1 + $3; }
|   exp '-' exp         { $$ = $1 - $3; }
|   exp '*' exp         { $$ = $1 * $3; }
|   exp '/' exp         { $$ = $1 / $3; }
|   '-' exp %prec NEG   { $$ = -$2; }
|   exp '^' exp         { $$ = pow($1, $3); }
|   '(' exp ')'         { $$ = $2; }
;

%%

struct init{
    char const *name;
    func_t *fun;
};

struct init const arith_funs[] = {
    {"atan", atan},
    {"circulo", circulo},
    {"cos", cos},
    {"cosh", cosh},
    {"cuadrado", cuadrado},
    {"exp", exp},
    {"ln", log},
    {"sin", sin},
    {"sqrt", sqrt},
    {0, 0}
};

symrec *sym_table;

static void init_table(void){
    for(int i = 0; arith_funs[i].name; i++){
        symrec *ptr = putsym(arith_funs[i].name, FUN);
        ptr->value.fun = arith_funs[i].fun;
    }
}

int main(void){  
    init_table();  
    yyparse();
    return 0;
}