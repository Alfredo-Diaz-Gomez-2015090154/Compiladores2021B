%{
#include <stdio.h>
#include "symbolTable.h"
#include "attribute.h"

void yyerror(char *mensaje){
    printf("Error: %s\n", mensaje);
}

void writeTabs(FILE *fp, int tabNumber){
    for(int i = 0; i < tabNumber; i++){
        fprintf(fp, "\t");
    }
}

FILE *output;
int identLevel = 1;

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
%nterm <int> math_expression
%nterm <symrec*> noun_expression

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

%%

input:
    %empty
|   input line
;

line:
    '\n'
|   statement_list '\n'
|   error '\n'                                          { yyerror; }
;

statement_list:
    statement
|   statement_list statement
;

statement:
    is_op
//|   make_op
//|   has_op
|   assign_number
|   if_statement
|   while_statement
;

noun_expression:
    NOUN                                                {
                                                            nounList = putNPNode(nounList, $1->name, 0);                                                                       
                                                        }
|   NOT NOUN                                            {
                                                            nounList = putNPNode(nounList, $2->name, 1);                                                                        
                                                        }
|   noun_expression AND noun_expression                 {
                                                            $$ = $1;
                                                            $$->next = $3;
                                                        }
;

property_expression:
    PROPERTY                                            {
                                                            propertyList = putNPNode(propertyList, $1->name, 0);                                                                       
                                                        }
|   NOT PROPERTY                                        {
                                                            propertyList = putNPNode(propertyList, $2->name, 1);                                                                        
                                                        }      
|   property_expression AND property_expression         
;

is_op:
    noun_expression IS property_expression              {   //Prototipo de regla semántica
                                                            printf("1.- Obtener el conjunto de 'nouns'.\n");
                                                            printf("2.- Obtener el conjunto de 'properties'.\n");                                                       
                                                            printf("3.- Aplicar el conjunto de 'properties' al conjunto de 'nouns'.\n");                                                            
                                                            for(NPNode *noun = nounList; noun; noun = noun->next){
                                                                printf("%s, %d\n", noun->name, noun->isNot);
                                                                writeTabs(output, identLevel);
                                                                fprintf(output, "var %ss = get_tree().get_nodes_in_group('%s')\n", noun->name, noun->name);
                                                                for(NPNode *property = propertyList; property; property = property->next){
                                                                    printf("%s, %d\n", noun->name, noun->isNot);
                                                                    writeTabs(output, identLevel);
                                                                    fprintf(output, "for %s_node in %ss:\n", noun->name, noun->name);
                                                                    writeTabs(output, identLevel);
                                                                    fprintf(output, "\t%s_node.is_%s = true\n", noun->name, property->name);
                                                                    fprintf(output, "\n");
                                                                }                                                                
                                                            }
                                                            
                                                            freeNPList(nounList);
                                                            nounList = NULL;
                                                            freeNPList(propertyList);
                                                            propertyList = NULL;

                                                            
                                                        }
;


assign_number:
    VAR IDENTIFIER IS math_expression                   { //Prototipo de regla semántica.
                                                            printf("1.- Calcular/Obtener el valor de 'math_expression'.\n");
                                                            printf("2.- Obtener la dirección de IDENTIFIER.\n");
                                                            printf("3.- Copiar el valor de 'math_expression' a la dirección de IDENTIFIER.\n");
                                                            
                                                            writeTabs(output, identLevel);
                                                            fprintf(output, "var %s = %d", $2->name, $4);
                                                            fprintf(output, "\n");


                                                        }          
;

math_expression:
    NUMBER                                              
|   '(' math_expression ')'                             { $$ = $2; }
|   IDENTIFIER                                          { $$ = $1->value.var; }
|   math_expression PLUS math_expression                { //Prototipo de regla semántica.
                                                            printf("Suma: %d\n", ($1 + $3));
                                                            printf("1.- Calcular/Obtener el valor de la primera 'math_expression'.\n");
                                                            printf("2.- Calcular/Obtener el valor de la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar la suma de ambas 'math_expression'.\n");
                                                        }
|   math_expression MINUS math_expression               { //Prototipo de regla semántica.
                                                            printf("1.- Calcular/Obtener el valor de la primera 'math_expression'.\n");
                                                            printf("2.- Calcular/Obtener el valor de la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar la diferencia de la primera 'math_expression' y la segunda 'math_expression'.\n");
                                                        }
|   math_expression TIMES math_expression               { //Prototipo de regla semántica.
                                                            printf("1.- Calcular/Obtener el valor de la primera 'math_expression'.\n");
                                                            printf("2.- Calcular/Obtener el valor de la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar el producto de ambas 'math_expression'.\n");
                                                        }
|   math_expression DIV_BY math_expression              { //Prototipo de regla semántica.
                                                            printf("Valor: %d\n", $3);
                                                            //printf("Division: %d\n", ($1/$3) );
                                                            if($3 == 0){
                                                                yyerror("División entre cero");
                                                                return 0;
                                                            }else{
                                                                printf("1.- Calcular/Obtener el valor de la primera 'math_expression'.\n");
                                                                printf("2.- Calcular/Obtener el valor de la segunda 'math_expression'.\n");
                                                                printf("3.- Evaluar la división de la primera 'math_expression' sobre la segunda 'math_expression'.\n");
                                                            }
                                                        }
;

if_statement:
    IF logical_expression THEN statement_list IF END        { //Prototipo de regla semántica.
                                                                printf("1.- Obtener/Evaluar 'logical_expression'.\n");
                                                                printf("2.- Obtener el conjunto de sentencias de 'statement'.\n");
                                                                printf("3.- Ejecutar el conjunto de sentencias de 'statement' en caso de que la evaluación de 'logical_expression sea True'.\n");
                                                            }
;

while_statement:
    WHILE logical_expression THEN statement_list WHILE END
;

logical_expression:
    math_logical_expression
//|   on_expression
|   is_op
|   logical_expression OR logical_expression            { //Prototipo de regla semántica.
                                                            printf("1.- Formar una expresión lógica compuesta de dos 'logical_expression'.\n");
                                                        }
|   logical_expression AND logical_expression           { //Prototipo de regla semántica.
                                                            printf("1.- Formar una expresión lógica compuesta de dos 'logical_expression'.\n");
                                                        }
|   NOT logical_expression                              { //Prototipo de regla semántica.
                                                            printf("1.- Invertir el valor lógico de 'logical_expression'.\n");
                                                        }
;

math_logical_expression:
    math_expression EQUALS math_expression              { //Prototipo de regla semántica.
                                                            printf("1.- Obtener/Calcular la primera 'math_expression'.\n");
                                                            printf("2.- Obtener/Calcular la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar si el valor de ambas 'math_expression' son iguales.\n");
                                                        }
|   math_expression SMALLER math_expression             { //Prototipo de regla semántica.
                                                            printf("1.- Obtener/Calcular la primera 'math_expression'.\n");
                                                            printf("2.- Obtener/Calcular la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar si el valor de ambas 'math_expression' son iguales.\n");
                                                        }
|   math_expression HIGHER math_expression              { //Prototipo de regla semántica.
                                                            printf("1.- Obtener/Calcular la primera 'math_expression'.\n");
                                                            printf("2.- Obtener/Calcular la segunda 'math_expression'.\n");
                                                            printf("3.- Evaluar si valor .");
                                                        }
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

int main(void){

    output = fopen("RuleChanger.gd", "w");

    if(output == NULL){
        printf("Error al abrir el archivo.");
    }else{
        printf("Excribiendo en archivo.\n");
        fputs("extends Node\n", output);
        fputs("func rule_changer():\n", output);
        printf("Escritura realizada.\n");

        init_table();
        yyparse();

        fclose(output);  
    }

    return 0;
}