%{
#include <stdio.h>
#include "symbolTable.h"
#include "attribute.h"

// <name>T; T al final por "Type".
//enum NodeType{NodeT, NumberT, IdentifierT, ArithmeticOperationT, AssignNumberT, StatementListT, InputT};

void yyerror(char *mensaje){
    printf("Error: %s\n", mensaje);
}

/*void writeTabs(FILE *fp, int tabNumber){
    for(int i = 0; i < tabNumber; i++){
        fprintf(fp, "\t");
    }
}*/

enum NodeType;

FILE *output;
int identLevel = 1;
Node* tree;

%}

%define api.value.type union
%token <symrec*> NOUN PROPERTY IDENTIFIER
%token <int> NUMBER
%token AND OR NOT
%token IF WHILE THEN END
%token PLUS MINUS TIMES DIV_BY
//%token IS HAS MAKE EQUALS
%token IS EQUALS
%token VAR
%token HIGHER SMALLER
%token ON
%nterm <Node*> math_expression assign_number statement statement_list s input line math_logical_expression logical_expression
if_statement while_statement noun_expression property_expression is_op

//%precedence IS
//%left MINUS PLUS OR
//%left TIMES DIV_BY AND
//%precedence NOT


%left IS

%left NOT
%left AND
%left OR


%left PLUS MINUS
%left TIMES DIV_BY

%start s

%%

s:
    input                                               { $$ = $1;
                                                          tree = $$;
                                                        }
;

input:
    %empty                                              { $$ = NULL; }
|   input line                                          { $$ = newNode(InputT, $1, $2); }
;

line:
    '\n'                                                { $$ = NULL; }
|   statement_list '\n'                                 { $$ = $1; }
|   error '\n'                                          { yyerror; }
;

statement_list:
    statement                                           { $$ = $1; }
|   statement_list statement                            { $$ = newNode(StatementListT, $1, $2 ); }
;

statement:
    is_op                                               { $$ = $1; }
|   assign_number                                       { $$ = $1; }
|   if_statement                                        { $$ = $1; }
|   while_statement                                     { $$ = $1; }
//|   make_op
//|   has_op
;

noun_expression:
    NOUN                                                { $$ = newNPNode(NPT, $1->name, 0, NULL); }
|   NOT NOUN                                            { $$ = newNPNode(NPT, $2->name, 1, NULL); }
|   noun_expression AND noun_expression                 {                                     
                                                            $$ = $3;
                                                            ((NPNode*)$$)->next = (NPNode*)$1;
                                                        }
;

property_expression:
    PROPERTY                                            { $$ = newNPNode(NPT, $1->name, 0, NULL); }
|   NOT PROPERTY                                        { $$ = newNPNode(NPT, $2->name, 1, NULL); }      
|   property_expression AND property_expression         {                                                            
                                                            $$ = $3;
                                                            ((NPNode*)$$)->next = (NPNode*)$1;
                                                        }
;

is_op:
    noun_expression IS property_expression              { $$ = newIsStatementNode(IsStatementT, $1, $3); }
;

assign_number:
    VAR IDENTIFIER IS math_expression                   { $$ = newAssignNumberNode(AssignNumberT, $2->name, $4); }          
;

math_expression:
    NUMBER                                              { $$ = newNumberNode(NumberT, $1); }
|   '(' math_expression ')'                             { $$ = newParenthesesArithmeticOperationNode(ParenthesesArithmeticOperationT, $2); }
|   IDENTIFIER                                          { $$ = newIdentifierNode(IdentifierT, $1->name); }
|   math_expression PLUS math_expression                { //Prototipo de regla semántica.
                                                        //    printf("Suma: %d\n", ($1 + $3));
                                                            //fprintf(output, "+ ");       
                                                            printf("1.- Calcular/Obtener el valor de la primera 'math_expression'.\n");
                                                            printf("2.- Calcular/Obtener el valor de la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar la suma de ambas 'math_expression'.\n");
                                                            $$ = newArithmeticOperationNode(ArithmeticOperationT, '+', $1, $3);
                                                        }
|   math_expression MINUS math_expression               { //Prototipo de regla semántica.
                                                            //fprintf(output, "- ");
                                                            printf("1.- Calcular/Obtener el valor de la primera 'math_expression'.\n");
                                                            printf("2.- Calcular/Obtener el valor de la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar la diferencia de la primera 'math_expression' y la segunda 'math_expression'.\n");
                                                            $$ = newArithmeticOperationNode(ArithmeticOperationT, '-', $1, $3);
                                                        }
|   math_expression TIMES math_expression               { //Prototipo de regla semántica.
                                                            //fprintf(output, "* ");
                                                            printf("1.- Calcular/Obtener el valor de la primera 'math_expression'.\n");
                                                            printf("2.- Calcular/Obtener el valor de la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar el producto de ambas 'math_expression'.\n");
                                                            $$ = newArithmeticOperationNode(ArithmeticOperationT, '*', $1, $3);
                                                        }
|   math_expression DIV_BY math_expression              { //Prototipo de regla semántica.
                                                            //fprintf(output, "/ ");
                                                            /*printf("Valor: %d\n", $3);
                                                            //printf("Division: %d\n", ($1/$3) );
                                                            if($3 == 0){
                                                                yyerror("División entre cero");
                                                                return 0;
                                                            }else{
                                                                printf("1.- Calcular/Obtener el valor de la primera 'math_expression'.\n");
                                                                printf("2.- Calcular/Obtener el valor de la segunda 'math_expression'.\n");
                                                                printf("3.- Evaluar la división de la primera 'math_expression' sobre la segunda 'math_expression'.\n");
                                                            }*/
                                                            $$ = newArithmeticOperationNode(ArithmeticOperationT, '/', $1, $3);
                                                        }
;

if_statement:
    IF logical_expression THEN statement_list IF END        { $$ = newIfStatementNode(IfStatementT, $2, $4); }
;

while_statement:
    WHILE logical_expression THEN statement_list WHILE END  { $$ = newWhileStatementNode(WhileStatementT, $2, $4); }
;

logical_expression:
    math_logical_expression                             { $$ = $1; }
//|   on_expression
|   is_op
|   logical_expression OR logical_expression            { $$ = newLogicalExpressionOperationNode(LogicalExpressionOperationT, $1, $3, "||"); }
|   logical_expression AND logical_expression           { $$ = newLogicalExpressionOperationNode(LogicalExpressionOperationT, $1, $3, "&&"); }
|   NOT logical_expression                              { printf("1.- Invertir el valor lógico de 'logical_expression'.\n"); }
;

math_logical_expression:
    math_expression EQUALS math_expression              { $$ = newMathLogicalExpressionNode(MathLogicalExpressionT, "==", $1, $3); }
|   math_expression SMALLER math_expression             { $$ = newMathLogicalExpressionNode(MathLogicalExpressionT, "<", $1, $3);  }
|   math_expression HIGHER math_expression              { $$ = newMathLogicalExpressionNode(MathLogicalExpressionT, ">", $1, $3);  }
;

/*
make_op:
    noun_expression MAKE NOUN                           {   //Prototipo de regla semántica
                                                            printf("1.- Obtener el conjunto de 'nouns'.\n");
                                                            printf("2.- Obtener el 'NOUN'.\n");
                                                            printf("3.- Establecer que el conjunto de 'nouns' creará el 'NOUN' especificado en cada paso t.\n");
                                                        }
;
*/

/*
has_op:
    noun_expression HAS NOUN                            {   //Prototipo de regla semántica
                                                            printf("1.- Obtener el conjunto de 'nouns'.\n");
                                                            printf("2.- Obtener el 'NOUN'.\n");
                                                            printf("3.- Establecer qué conjunto de 'nouns' se convertirán en cierto 'NOUN' cuando una instancia de estos desaparezcan.\n");
                                                        }
;
*/

/*
on_expression:
    on_noun_expression ON NOUN                          { //Prototipo de regla semántica.
                                                            printf("1.- Obtener el valor 'on_noun_expression'.\n");
                                                            printf("2.- Obtener el 'NOUN'.\n");
                                                            printf("3.- Verificar que alguno de los 'NOUNS' que formen a 'on_noun_expression' se encuntra sobre un bloque de tipo 'NOUN'.\n");
                                                        }
;
*/

/*
on_noun_expression:
    noun_expression
|   on_noun_expression OR on_noun_expression
;
*/

%%

struct init{
    char const *name;
};

struct init const nouns[] = {
    {"ufo"}, {"rock"}, {"lava"}, {"flag"}, {"water"}, {"grass"}, 
    {"love"}, {"wall"}, {"skull"}, {"star"}, {"algae"}, 
    {0}
};

struct init const properties[] = {
    {"you"}, {"push"}, {"stop"}, {"death"}, {"float"}, 
    {"blue"}, {"red"}, {"tele"}, {"win"}, {"fall"},
    {"pull"}, {"up"}, {"swap"}, {"ship"}, {"best"}, 
    {0}
};

symrec *sym_table;
NPNode *propertyList;
NPNode *nounList;

static void init_table(void){
    for(int i = 0; nouns[i].name; i++){
        symrec *ptr = putsym(nouns[i].name, NOUN);
    }

    for(int i = 0; properties[i].name; i++){
        symrec *ptr = putsym(properties[i].name, PROPERTY);
    }

}

int main(){

    output = fopen("RuleChanger.gd", "w");

    if(output == NULL){
        printf("Error al abrir el archivo.");
    }else{
        //printf("Excribiendo en archivo.\n");
        fputs("extends Node\n\n", output);
        fputs("func rule_changer():\n", output);
        //printf("Escritura realizada.\n");

        init_table();
        yyparse();

        //printf("\nTipo: %d\n", tree->type);
        generateCode(output, tree, 1);

        fclose(output);  
    }

    return 0;
}