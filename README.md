# MOPL
My Own Programming Language

### BNF
```bnf
program : statements

statements : statement
           | statements statement

statement : attribution SEMI
          | if_else SEMI
          | expression SEMI
          | var_declaration SEMI
          | while SEMI
          | write SEMI
          | writeln SEMI

attribution : IDEN EQU expression

if_else : IF LPAR rel_expression RPAR BEGIN statements END
        | IF LPAR rel_expression RPAR BEGIN statements END ELSE BEGIN statements END

expression : term
           | term PLUS term
           | term MIN term
           | term OR term

var_declaration : type IDEN

while : WHILE LPAR rel_expression RPAR DO BEGIN statement_list END

write : WRITE LPAR expression RPAR

writeln : WRITE LPAR expression RPAR NEWL

rel_expression : expression LT expression
               | expression LTE expression
               | expression GT expression
               | expression GTE expression
               | expression DEQU expression
               | expression NEQU expression

term : factor
     | factor MULT factor
     | factor DIV factor
     | factor AND factor

factor : NUMB
       | IDEN
       | LPAR expression RPAR

type : INTEGER
```