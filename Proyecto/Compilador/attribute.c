#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "attribute.h"

NPNode *putNPNode(NPNode *list, char const *name, int isNot){
    printf("Creando nodo\n");
    NPNode *newNoun = (NPNode*)malloc(sizeof(NPNode));
    newNoun->name = strdup(name);
    newNoun->isNot = isNot;
    printf("Asignando siguiente\n");
    newNoun->next = list;
    printf("Nueva cabeza\n");
    //list = newNoun;
    return newNoun;
}

NPNode *getNPNode(NPNode *list, char const *name){
    for(NPNode *noun = list; noun; noun = noun->next){
        if(strcmp(noun->name, name) == 0){
            return noun;
        }
        return NULL;
    }
}

void freeNPList(NPNode *list){
    NPNode *nextNoun = list->next;
    while(nextNoun){
        free(list);
        list = nextNoun;
        nextNoun = list->next;
    }
    free(list);
}