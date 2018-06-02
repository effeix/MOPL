import ply.lex as lex
import ply.yacc as yacc

############################# LEXER #############################
reserved = {
    w: w.upper() for w in [
        "and",
        "begin",
        "do",
        "else",
        "end",
        "if",
        "integer",
        "not",
        "or",
        "write",
        "writeln",
        "program",
        "read",
        "then",
        "var",
        "while"
    ]
}

tokens = [
    'COMM',  # comment
    'COMMA', # ,
    'DEQU',  # ==
    'DIV',   # /
    'DOT',   # .
    'EQU',   # =
    'COL',   # :
    'GT',    # >
    'GTE',   # >=
    'IDEN',  # name
    'LPAR',  # (
    'LT',    # <
    'LTE',   # <=
    'MIN',   # -
    'MULT',  # *
    'NEQU',  # !=
    'NUMB',  # number
    'PLUS',  # +
    'RPAR',  # )
    'SEMI',  # ;
    'SPACE', # space char
    'TAB',   # tab char
] + list(reserved.values())

t_COMMA = r','
t_COL   = r':'
t_DEQU  = r'=='
t_DIV   = r'/'
t_DOT   = r'\.'
t_EQU   = r'='
t_GT    = r'>'
t_GTE   = r'>='
t_LPAR  = r'\('
t_LT    = r'<'
t_LTE   = r'<='
t_MIN   = r'-'
t_MULT  = r'\*'
t_NEQU  = r'!='
t_PLUS  = r'\+'
t_RPAR  = r'\)'
t_SEMI  = r';'
t_ignore_COMM = r'(\$(?s).*\$)' # comment syntax: $ ... $
t_ignore_TAB = r'\t'
t_ignore_SPACE = r'\s'


def t_NUMB(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFIER(t):
     r'[a-zA-Z_][a-zA-Z0-9_]*'
     t.type = reserved.get(t.value, 'IDEN')
     return t


def t_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)


def t_error(t):
    exit(f"Error: invalid token {t.value[0]}")


lexer = lex.lex()


############################# PARSER #############################
precedence = (
    ('left','PLUS','MIN'),
    ('left','MULT','DIV'),
    # ('right','UMINUS'),
)


def p_program(p):
    """
    program : statements
    """
    pass


def p_statements(p):
    """
    statements : statement
               | statements statement
    """
    pass


def p_statement(p):
    """
    statement : attribution SEMI
              | if_else SEMI
              | expression SEMI
              | var_declaration SEMI
              | while SEMI
              | write SEMI
    """
    pass


def p_attribution(p):
    """
    attribution : IDEN EQU expression
    """

def p_if_else(p):
    """
    if_else : IF LPAR rel_expression RPAR THEN BEGIN statements END
            | IF LPAR rel_expression RPAR THEN BEGIN statements END ELSE BEGIN statements END
    """
    pass


def p_expression(p):
    """
    expression : term
               | term PLUS term
               | term MIN term
               | term OR term
    """
    pass

def p_var_declaration(p):
    """
    var_declaration : type IDEN
    """
    pass


def p_while(p):
    """
    while : WHILE LPAR rel_expression RPAR DO BEGIN statements END
    """
    pass


def p_write(p):
    """
    write : WRITE LPAR expression RPAR
    """
    pass


def p_rel_expression(p):
    """
    rel_expression : expression LT expression
                   | expression LTE expression
                   | expression GT expression
                   | expression GTE expression
                   | expression DEQU expression
                   | expression NEQU expression
    """
    pass


def p_term(p):
    """
    term : factor
         | factor MULT factor
         | factor DIV factor
         | factor AND factor
    """
    pass


def p_factor(p):
    """
    factor : NUMB
           | IDEN
           | LPAR expression RPAR
    """
    pass


def p_type(p):
    """
    type : INTEGER
    """
    pass


def p_error(p):
    ptype = p.type
    pvalue = p.value if ptype == "IDEN" else ''
    exit(f"Syntax error at {ptype} {pvalue}")


parser = yacc.yacc()

with open('test.pas', 'r') as f:

    program = f.read()
    print("\n--------------------\n")
    print(program)
    print("\n--------------------\n")

    parser.parse(program)

    print("Done!")