
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
