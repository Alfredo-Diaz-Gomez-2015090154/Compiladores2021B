enum NodeType{NodeT, NumberT, IdentifierT, ArithmeticOperationT, ParenthesesArithmeticOperationT, AssignNumberT, StatementListT, InputT,
                MathLogicalExpressionT, LogicalExpressionOperationT, IfStatementT
            };

extern NodeType;

struct Node{
    int type;
    struct Node *leftChild;
    struct Node *rightChild;
};

typedef struct Node Node;

struct NumberNode{
    int type;
    int value;
};

typedef struct NumberNode NumberNode;

struct IdentifierNode{
    int type;
    char *name;
};

typedef struct IdentifierNode IdentifierNode;

struct ArithmeticOperationNode{
    int type;
    char operation;
    Node *leftChild;
    Node *rightChild;
};

typedef struct ArithmeticOperationNode ArithmeticOperationNode;

struct AssignNumberNode{
    int type;
    char *name;
    Node *mathExpression;
};

typedef struct AssignNumberNode AssignNumberNode;

struct ParenthesesArithmeticOperationNode{
    int type;
    Node *mathExpression;
};

typedef struct ParenthesesArithmeticOperationNode ParenthesesArithmeticOperationNode;

struct MathLogicalExpressionNode{
    int type;
    Node *leftMathExpression;
    Node *rightMathExpression;
    char *operation;
};

typedef struct MathLogicalExpressionNode MathLogicalExpressionNode;

struct LogicalExpressionOperationNode{
    int type;
    Node *leftLogicalExp;
    Node *rightLogicalExp;
    char *operation;
};

typedef struct LogicalExpressionOperationNode LogicalExpressionOperationNode;

struct IfStatementNode{
    int type;
    Node *logicalExpression;
    Node *statements;
};

typedef struct IfStatementNode IfStatementNode;


Node *newNode(int type, Node *leftChild, Node *rightChild);
Node *newNumberNode(int type, int value);
Node *newIdentifierNode(int type, char *name);
Node *newArithmeticOperationNode(int type, char operation, Node *leftChild, Node *rightChild);
Node *newAssignNumberNode(int type, char *name, Node *mathExpression);
Node *newParenthesesArithmeticOperationNode(int type, Node *mathExpression);
Node *newMathLogicalExpressionNode(int type, char *operation, Node *leftMathExpression, Node *rightMathExpression);
Node *newLogicalExpressionOperationNode(int type, Node *leftLogicalExp, Node *rightLogicalExp, char *operation);
Node *newIfStatementNode(int type, Node *logicalExpression, Node *statements);

void generateCode(FILE *output, Node *node, int indentLevel);
void generateCodeMathExpression(FILE *output, Node *mathExpression, int indentLevel);
void generateCodeMathLogicalExpression(FILE *output, Node *mathLogicalExpression, int indentLevel);
void generateCodeLogicalExpression(FILE *output, Node *logicalExpression, int indentLevel);
void generateCodeAssignNumber(FILE *output, Node *assignNumber, int indentLevel);
void generateCodeIf(FILE *output, Node *ifNode, int indentLevel);

void writeTabs(FILE *fp, int tabNumber);

//NPNode = NounPropertyNoude.
//Utilizado para el seguimiento de "Nouns" y "Properties" cuando se
//sube en el árbol.
struct NPNode{
    char *name;
    int isNot;
    struct NPNode *next;
};

typedef struct NPNode NPNode;

extern NPNode *nounList;
extern NPNode *propertyList;

NPNode *putNPNode(NPNode *list, char const *name, int isNot);
NPNode *getNPNode(NPNode *list, char const *name);
void freeNPList(NPNode *list);
