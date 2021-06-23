struct symrec{
    char *name;
    int type;            //Tipo.(IDENTIFIER, NOUN, PROPERTY)
    union{
        int var;         //Valor de IDENTIFIER.
    } value;
    struct symrec *next;
};

typedef struct symrec symrec;

extern symrec *sym_table;

symrec *putsym(char const *name, int sym_type);
symrec *getsym(char const *name);
void freeSymbolTable();