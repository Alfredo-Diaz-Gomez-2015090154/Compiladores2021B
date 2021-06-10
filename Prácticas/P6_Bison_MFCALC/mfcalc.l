%{
#include "tablaSimbolos.h"
#include "mfcalc.tab.h"
%}

D   [0-9]

%%
{D}*"."{D}+[ ]?"+"[ ]?"j"{D}*"."{D}+        { printf("Complejo positivo."); }
{D}*"."{D}+[ ]?"-"[ ]?"j"{D}*"."{D}+        { printf("Complejo negativo."); }
{D}*"."{D}+                                 { yylval.NUM = atof(yytext); return NUM; }
[a-zA-Z][a-zA-Z0-9]*                        {   symrec *s = getsym(yytext);
                                                if(!s){
                                                    s = putsym(yytext, VAR);
                                                    yylval.VAR = s;
                                                }else{
                                                    if(s->type == VAR){
                                                        yylval.VAR = s;
                                                    }else{
                                                        yylval.FUN = s;
                                                    }
                                                }                                                                
                                                return s->type;
                                            }
[+]                                         { return '+'; }
[-]                                         { return '-'; }
[*]                                         { return '*'; }
[/]                                         { return '/'; }
"^"                                         { return '^'; }
[=]                                         { return '='; }
[(]                                         { return '('; }
[)]                                         { return ')'; }
\n                                          { return '\n'; }
[ ]*
.
%%