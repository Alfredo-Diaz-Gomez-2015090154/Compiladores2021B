enum NodeType{NodeT, NumberT, IdentifierT, ArithmeticOperationT, ParenthesesArithmeticOperationT, AssignNumberT, ModifyVariableT, 
                StatementListT, InputT, MathLogicalExpressionT, LogicalExpressionOperationT, IfStatementT, WhileStatementT, NPT, 
                IsStatementT
            };

//extern NodeType;

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

struct ModifyVariableNode{
    int type;
    char *name;
    Node *mathExpression;
};

typedef struct ModifyVariableNode ModifyVariableNode;

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

struct WhileStatementNode{
    int type;
    Node *logicalExpression;
    Node *statements;
};

typedef struct WhileStatementNode WhileStatementNode;

struct NPNode{
    int type;
    char *name;
    int isNot;
    struct NPNode *next;
};

typedef struct NPNode NPNode;

struct IsStatementNode{
    int type;
    struct NPNode *nouns;
    struct NPNode *properties;
};

typedef struct IsStatementNode IsStatementNode;


Node *newNode(int type, Node *leftChild, Node *rightChild);
Node *newNumberNode(int type, int value);
Node *newIdentifierNode(int type, char *name);
Node *newArithmeticOperationNode(int type, char operation, Node *leftChild, Node *rightChild);
Node *newAssignNumberNode(int type, char *name, Node *mathExpression);
Node *newParenthesesArithmeticOperationNode(int type, Node *mathExpression);
Node *newMathLogicalExpressionNode(int type, char *operation, Node *leftMathExpression, Node *rightMathExpression);
Node *newLogicalExpressionOperationNode(int type, Node *leftLogicalExp, Node *rightLogicalExp, char *operation);
Node *newIfStatementNode(int type, Node *logicalExpression, Node *statements);
Node *newWhileStatementNode(int type, Node *logicalExpression, Node *statements);
Node *newNPNode(int type, char *name, int isNot, struct NPNode *next);
Node *newIsStatementNode(int type, struct Node *nouns, struct Node *properties);
Node *newModifyVariableNode(int type, char *name, Node *mathExpression);

void generateCode(FILE *output, Node *node, int indentLevel);
void generateCodeMathExpression(FILE *output, Node *mathExpression, int indentLevel);
void generateCodeMathLogicalExpression(FILE *output, Node *mathLogicalExpression, int indentLevel);
void generateCodeLogicalExpression(FILE *output, Node *logicalExpression, int indentLevel);
void generateCodeAssignNumber(FILE *output, Node *assignNumber, int indentLevel);
void generateCodeModifyVariable(FILE *output, Node *modifyNumber, int indentLevel);
void generateCodeIf(FILE *output, Node *ifNode, int indentLevel);
void generateCodeWhile(FILE *output, Node *whileNode, int indentLevel);
void generateCodeIsOp(FILE *output, Node *isOpNode, int indentLevel);
void generateCodeIsYou(FILE *output, char *nounName, NPNode *noun, NPNode *property, int indentLevel);

void writeTabs(FILE *fp, int tabNumber);
