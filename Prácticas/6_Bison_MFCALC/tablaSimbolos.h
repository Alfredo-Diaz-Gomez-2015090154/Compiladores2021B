typedef double (func_t) (double);


struct symrec{
    char *name; //Nombre del símbolo.
    int type;   //Tipo del símbolo (VAR o FUN).
    union{
        double var;     //Valor de un VAR.
        func_t *fun;    //Valor de un FUN.
    } value;
    struct symrec *next;
};

typedef struct symrec symrec;

extern symrec *sym_table;

symrec *putsym(char const *name, int sym_type);
symrec *getsym(char const *name);