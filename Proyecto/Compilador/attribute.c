#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "attribute.h"

enum NodeType;


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

Node *newModifyVariableNode(int type, char *name, Node *mathExpression){
    ModifyVariableNode *newModifyVariable = (ModifyVariableNode*)malloc(sizeof(ModifyVariableNode));
    newModifyVariable->type = type;
    newModifyVariable->name = strdup(name);
    newModifyVariable->mathExpression = mathExpression;
    return (Node*)newModifyVariable;    
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

Node *newWhileStatementNode(int type, Node *logicalExpression, Node *statements){
    WhileStatementNode *newWhile = (WhileStatementNode*)malloc(sizeof(WhileStatementNode));
    newWhile->type = type;
    newWhile->logicalExpression = logicalExpression;
    newWhile->statements = statements;
    return (Node*)newWhile;
}

Node *newNPNode(int type, char *name, int isNot, struct NPNode *next){
    NPNode *newNPNode = (NPNode*)malloc(sizeof(NPNode));
    newNPNode->type = type;
    newNPNode->name = strdup(name);
    newNPNode->isNot = isNot;
    newNPNode->next = next;
    return (Node*)newNPNode;
}

Node *newIsStatementNode(int type, struct Node *nouns, struct Node *properties){
    IsStatementNode *newIsNode = (IsStatementNode*)malloc(sizeof(IsStatementNode));
    newIsNode->type = type;
    newIsNode->nouns = (NPNode*)nouns;
    newIsNode->properties = (NPNode*)properties;
    return (Node*)newIsNode;
}

void generateCode(FILE *output, Node *node, int indentLevel){

    //printf("Generando código 'general'. Soy un %d\n", node->type);

    switch(node->type){
        case InputT:
        case StatementListT:
            if(node->leftChild != NULL){
                generateCode(output, node->leftChild, indentLevel);
            }

            if(node->rightChild != NULL){
                generateCode(output, node->rightChild, indentLevel);
            }     
        break;

        /*case StatementListT:
            if(node->leftChild != NULL){
                generateCode(output, node->leftChild, indentLevel);
            }

            if(node->rightChild != NULL){
                generateCode(output, node->rightChild, indentLevel);
            } 
        break;*/

        case IfStatementT:
            generateCodeIf(output, node, indentLevel);
        break;

        case AssignNumberT:
            generateCodeAssignNumber(output, node, indentLevel);
        break;

        case ModifyVariableT:
            generateCodeModifyVariable(output, node, indentLevel);
        break;

        case WhileStatementT:
            generateCodeWhile(output, node, indentLevel);
        break;

        case IsStatementT:
            //printf("Soy un IS :D\n");
            generateCodeIsOp(output, node, indentLevel);
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
    //printf("Generando logical expression... \n");
    if(logicalExpression->type == LogicalExpressionOperationT){
        //printf("    Generando logical expression compuesta... \n");
        //printf("        Generando logical expression izq... \n");
        generateCodeLogicalExpression(output, ((LogicalExpressionOperationNode*)logicalExpression)->leftLogicalExp, indentLevel);
        //printf("        Generando logical expression operador... \n");
        fprintf(output, " %s ", ((LogicalExpressionOperationNode*)logicalExpression)->operation);
        //printf("        Generando logical expression izq... \n");
        generateCodeLogicalExpression(output, ((LogicalExpressionOperationNode*)logicalExpression)->rightLogicalExp, indentLevel);
    }else if(logicalExpression->type == MathLogicalExpressionT){
        //printf("Generando math logical expression... \n");
        generateCodeMathLogicalExpression(output, logicalExpression, indentLevel);
    }
}

void generateCodeAssignNumber(FILE *output, Node *assignNumber, int indentLevel){
    writeTabs(output, indentLevel);
    fprintf(output, "var %s = ", ((AssignNumberNode*)assignNumber)->name);
    generateCodeMathExpression(output, ((AssignNumberNode*)assignNumber)->mathExpression, indentLevel);
    fprintf(output, "\n");
}

void generateCodeModifyVariable(FILE *output, Node *modifyNumber, int indentLevel){
    writeTabs(output, indentLevel);
    fprintf(output, "%s = ", ((ModifyVariableNode*)modifyNumber)->name);
    generateCodeMathExpression(output, ((ModifyVariableNode*)modifyNumber)->mathExpression, indentLevel);
    fprintf(output, "\n");    
}

void generateCodeIf(FILE *output, Node *ifNode, int indentLevel){
    //printf("Generando if... \n");
    writeTabs(output, indentLevel);
    fprintf(output, "if ");
    //printf("    Generando logical expression... \n");
    generateCodeLogicalExpression(output, ((IfStatementNode*)ifNode)->logicalExpression, indentLevel);
    //printf("    Generando salto de línea... \n");
    fprintf(output, ":\n");
    //printf("    Generando statements... \n");
    generateCode(output, ((IfStatementNode*)ifNode)->statements, indentLevel + 1);
}

void generateCodeWhile(FILE *output, Node *whileNode, int indentLevel){
    writeTabs(output, indentLevel);
    fprintf(output, "while ");
    generateCodeLogicalExpression(output, ((IfStatementNode*)whileNode)->logicalExpression, indentLevel);
    fprintf(output, ":\n");
    generateCode(output, ((IfStatementNode*)whileNode)->statements, indentLevel + 1);
    writeTabs(output, indentLevel);
    fprintf(output, "\tyield(world_controller_node, \"movement_s\")");
}

void generateCodeIsOp(FILE *output, Node *isOpNode, int indentLevel){

    fprintf(output, "\n");

    for(NPNode *noun = ((IsStatementNode*)isOpNode)->nouns; noun; noun = noun->next){
        writeTabs(output, indentLevel);
        fprintf(output, "var %ss = get_tree().get_nodes_in_group('%s')\n", noun->name, noun->name);
        writeTabs(output, indentLevel);
        fprintf(output, "for %s_node in %ss:\n", noun->name, noun->name);
        for(NPNode *property = ((IsStatementNode*)isOpNode)->properties; property; property = property->next){
            //printf("Valor evaluación: %d\n", !(noun->isNot ^ property->isNot));
            if(strcmp(property->name, "you") == 0){
                generateCodeIsYou(output, noun->name, noun, property, indentLevel);
            }else{
                if(property->name)
                writeTabs(output, indentLevel);
                if(!(noun->isNot ^ property->isNot) == 1){
                    fprintf(output, "\t%s_node.is_%s = true\n", noun->name, property->name);
                }else{
                    fprintf(output, "\t%s_node.is_%s = false\n", noun->name, property->name);
                }
                fprintf(output, "\n");
            }
        }
        
    }
}

void generateCodeIsYou(FILE *output, char *nounName, NPNode *noun, NPNode *property, int indentLevel){
    if(!(noun->isNot ^ property->isNot) == 1){
        writeTabs(output, indentLevel);
        fprintf(output, "\tif !%s_node.is_in_group(\"you\"):\n", noun->name);
        writeTabs(output, indentLevel);
        fprintf(output, "\t\t%s_node.add_to_group(\"you\"):\n", noun->name);
        writeTabs(output, indentLevel);
        fprintf(output, "\t%s_node.is_you = true\n", noun->name);
    }else{
        writeTabs(output, indentLevel);
        fprintf(output, "\tif %s_node.is_in_group(\"you\"):\n", noun->name);
        writeTabs(output, indentLevel);
        fprintf(output, "\t\t%s_node.remove_from_group(\"you\"):\n", noun->name);
        writeTabs(output, indentLevel);
        fprintf(output, "\t%s_node.is_you = false\n", noun->name);
    }
    fprintf(output, "\n");
}

void writeTabs(FILE *fp, int tabNumber){
    for(int i = 0; i < tabNumber; i++){
        fprintf(fp, "\t");
    }
}