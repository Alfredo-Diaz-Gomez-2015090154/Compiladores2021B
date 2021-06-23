#include <stdlib.h> //Malloc, Realloc.
#include <string.h> //strlen
#include <stdio.h>
#include "symbolTable.h"

symrec *putsym(char const *name, int sym_type){
    symrec *res = (symrec*)malloc(sizeof(symrec));
    res->name = strdup(name);
    res->type = sym_type;
    res->value.var = 0;
    res->next = sym_table;
    sym_table = res;
    return res;
}

symrec *getsym(char const *name){
    for(symrec *p = sym_table; p; p = p->next){
        if(strcmp(p->name, name) == 0){
            return p;
        }
    }
    return NULL;
}

void freeSymbolTable(){
    printf("%s\n", sym_table->name);
    symrec *nextSymbol = nextSymbol->next;
    while(nextSymbol){
        free(sym_table);
        sym_table = nextSymbol;
        printf("%s\n", sym_table->name);
        symrec *nextSymbol = nextSymbol->next;
    }
    free(sym_table);
}