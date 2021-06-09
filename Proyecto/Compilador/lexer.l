%{
#include "symbolTable.h"
#include "grammar.tab.h"
%}

%%

"and"           { return AND; }
"end"           { return END; }
"equals"        { return EQUALS; }
"if"            { return IF; }
"is"            { return IS; }
"not"           { return NOT; }
"on"            { return ON; }
"or"            { return OR; }
"then"          { return THEN; }
"var"           { return VAR; }
"while"         { return WHILE; }
"plus"          { return PLUS; }
"minus"         { return MINUS; }
"times"         { return TIMES; }
">"             { return SMALLER; }
"<"             { return HIGHER; }
"("             { return '('; }
")"             { return ')'; }

[1-9][0-9]*     { yylval.NUMBER = atoi(yytext); return NUMBER; }
[a-z][a-z0-9]*  {   symrec *s = getsym(yytext); 
                    if(!s){
                        s = putsym(yytext, IDENTIFIER);
                        yylval.IDENTIFIER = s;
                    }else{
                        if(s->type == NOUN){
                            yylval.NOUN = s;
                        }else if(s->type == PROPERTY){
                            yylval.PROPERTY = s;
                        }else{
                            yylval.IDENTIFIER = s;
                        }
                    }
                    return s->type;
                }
\n              {   return '\n'; }
[ ]*
.

%%