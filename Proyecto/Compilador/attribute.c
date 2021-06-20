#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "attribute.h"

enum NodeType;

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


Node *newNode(int type, Node *leftChild, Node *rightChild){
    Node *newNode = (Node*)malloc(sizeof(Node));
    newNode->type = type;
    newNode->leftChild = leftChild;
    newNode->rightChild = rightChild;
    return newNode;
}

Node *newNumberNode(int type, int value){
    NumberNode *newNumberNode = (NumberNode*)malloc(sizeof(NumberNode));
    newNumberNode->type = type;
    newNumberNode->value = value;
    return (Node*)newNumberNode;
}

Node *newIdentifierNode(int type, char *name){
    IdentifierNode *newIdentifierNode = (IdentifierNode*)malloc(sizeof(IdentifierNode));
    newIdentifierNode->type = type;
    newIdentifierNode->name = strdup(name);
    return (Node*)newIdentifierNode;
}

Node *newArithmeticOperationNode(int type, char operation, Node *leftChild, Node *rightChild){
    ArithmeticOperationNode *newArithOpNode = (ArithmeticOperationNode*)malloc(sizeof(ArithmeticOperationNode));
    newArithOpNode->type = type;
    newArithOpNode->operation = operation;
    newArithOpNode->leftChild = leftChild;
    newArithOpNode->rightChild = rightChild;
    return (Node*)newArithOpNode;
}

Node *newAssignNumberNode(int type, char *name, Node *mathExpression){
    AssignNumberNode *newAssignNumber = (AssignNumberNode*)malloc(sizeof(AssignNumberNode));
    newAssignNumber->type = type;
    newAssignNumber->name = strdup(name);
    newAssignNumber->mathExpression = mathExpression;
    return (Node*)newAssignNumber;
}

Node *newParenthesesArithmeticOperationNode(int type, Node *mathExpression){
    ParenthesesArithmeticOperationNode *newParArithExpr = (ParenthesesArithmeticOperationNode*)malloc(sizeof(ParenthesesArithmeticOperationNode));
    newParArithExpr->type = type;
    newParArithExpr->mathExpression = mathExpression;
    return (Node*)newParArithExpr;
}

Node *newMathLogicalExpressionNode(int type, char *operation, Node *leftMathExpression, Node *rightMathExpression){
    MathLogicalExpressionNode *newMathLogExp = (MathLogicalExpressionNode*)malloc(sizeof(MathLogicalExpressionNode));
    newMathLogExp->type = type;
    newMathLogExp->leftMathExpression = leftMathExpression;
    newMathLogExp->rightMathExpression = rightMathExpression;
    newMathLogExp->operation = strdup(operation);
    return (Node*)newMathLogExp;
}

Node *newLogicalExpressionOperationNode(int type, Node *leftLogicalExp, Node *rightLogicalExp, char *operation){
    LogicalExpressionOperationNode *newLogExpOp = (LogicalExpressionOperationNode*)malloc(sizeof(LogicalExpressionOperationNode));
    newLogExpOp->type = type;
    newLogExpOp->leftLogicalExp = leftLogicalExp;
    newLogExpOp->rightLogicalExp = rightLogicalExp;
    newLogExpOp->operation = strdup(operation);
    return (Node*)newLogExpOp;
}

Node *newIfStatementNode(int type, Node *logicalExpression, Node *statements){
    IfStatementNode *newIf = (IfStatementNode*)malloc(sizeof(IfStatementNode));
    newIf->type = type;
    newIf->logicalExpression = logicalExpression;
    newIf->statements = statements;
    return (Node*)newIf;
}

void generateCode(FILE *output, Node *node, int indentLevel){

    printf("Generando código 'general'. Soy un %d\n", node->type);

    switch(node->type){
        case InputT:
            if(node->leftChild != NULL){
                generateCode(output, node->leftChild, indentLevel);
            }else{
                printf("\tNulo izquierdo.\n");
            }

            if(node->rightChild != NULL){
                generateCode(output, node->rightChild, indentLevel);
            }else{
                printf("\tNulo derecho.\n");
            }        
        break;

        case StatementListT:
            if(node->leftChild != NULL){
                generateCode(output, node->leftChild, indentLevel);
            }

            if(node->rightChild != NULL){
                generateCode(output, node->rightChild, indentLevel);
            } 
        break;

        case IfStatementT:
            generateCodeIf(output, node, indentLevel);
        break;

        case AssignNumberT:
            generateCodeAssignNumber(output, node, indentLevel);
        break;

    }

}


void generateCodeMathExpression(FILE *output, Node *mathExpression, int indentLevel){
    if(mathExpression->type == ArithmeticOperationT){
        generateCodeMathExpression(output, mathExpression->leftChild, indentLevel);    
        fprintf(output, " %c ", ((ArithmeticOperationNode*)mathExpression)->operation);
        generateCodeMathExpression(output, mathExpression->rightChild, indentLevel);
    }else if(mathExpression->type == NumberT ){
        fprintf(output, " %d ", ((NumberNode*)mathExpression)->value);
    }else if(mathExpression->type == IdentifierT){
        fprintf(output, " %s ", ((IdentifierNode*)mathExpression)->name);
    }else if(mathExpression->type == ParenthesesArithmeticOperationT){
        fprintf(output, "(");
        generateCodeMathExpression(output, ((ParenthesesArithmeticOperationNode*)mathExpression)->mathExpression, indentLevel);
        fprintf(output, ")");
    }
}

void generateCodeMathLogicalExpression(FILE *output, Node *mathLogicalExpression, int indentLevel){
    generateCodeMathExpression(output, ((MathLogicalExpressionNode*)mathLogicalExpression)->leftMathExpression, indentLevel);
    fprintf(output, " %s ", ((MathLogicalExpressionNode*)mathLogicalExpression)->operation);
    generateCodeMathExpression(output, ((MathLogicalExpressionNode*)mathLogicalExpression)->rightMathExpression, indentLevel);
}

void generateCodeLogicalExpression(FILE *output, Node *logicalExpression, int indentLevel){
    printf("Generando logical expression... \n");
    if(logicalExpression->type == LogicalExpressionOperationT){
        printf("    Generando logical expression compuesta... \n");
        printf("        Generando logical expression izq... \n");
        generateCodeLogicalExpression(output, ((LogicalExpressionOperationNode*)logicalExpression)->leftLogicalExp, indentLevel);
        printf("        Generando logical expression operador... \n");
        fprintf(output, " %s ", ((LogicalExpressionOperationNode*)logicalExpression)->operation);
        printf("        Generando logical expression izq... \n");
        generateCodeLogicalExpression(output, ((LogicalExpressionOperationNode*)logicalExpression)->rightLogicalExp, indentLevel);
    }else if(logicalExpression->type == MathLogicalExpressionT){
        printf("Generando math logical expression... \n");
        generateCodeMathLogicalExpression(output, logicalExpression, indentLevel);
    }
}

void generateCodeAssignNumber(FILE *output, Node *assignNumber, int indentLevel){
    writeTabs(output, indentLevel);
    fprintf(output, "var %s = ", ((AssignNumberNode*)assignNumber)->name);
    generateCodeMathExpression(output, ((AssignNumberNode*)assignNumber)->mathExpression, indentLevel);
    fprintf(output, "\n");
}

void generateCodeIf(FILE *output, Node *ifNode, int indentLevel){
    printf("Generando if... \n");
    writeTabs(output, indentLevel);
    fprintf(output, "if ");
    printf("    Generando logical expression... \n");
    generateCodeLogicalExpression(output, ((IfStatementNode*)ifNode)->logicalExpression, indentLevel);
    printf("    Generando salto de línea... \n");
    fprintf(output, ":\n");
    printf("    Generando statements... \n");
    generateCode(output, ((IfStatementNode*)ifNode)->statements, indentLevel + 1);
}

void writeTabs(FILE *fp, int tabNumber){
    for(int i = 0; i < tabNumber; i++){
        fprintf(fp, "\t");
    }
}