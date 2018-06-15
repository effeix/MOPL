import ply.lex as lex
import ply.yacc as yacc

# ############################ LEXER ############################# #
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
    'COMM',   # comment
    'COMMA',  # ,
    'DEQU',   # ==
    'DIV',    # /
    'DOT',    # .
    'EQU',    # =
    'COL',    # :
    'GT',     # >
    'GTE',    # >=
    'IDEN',   # name
    'LPAR',   # (
    'LT',     # <
    'LTE',    # <=
    'MIN',    # -
    'MULT',   # *
    'NEQU',   # !=
    'NUMB',   # number
    'PLUS',   # +
    'RPAR',   # )
    'SEMI',   # ;
    'SPACE',  # space char
    'TAB',    # tab char
] + list(reserved.values())

t_COMMA = r','
t_COL = r':'
t_DEQU = r'\=\='
t_DIV = r'/'
t_DOT = r'\.'
t_EQU = r'='
t_GT = r'>'
t_GTE = r'\>\='
t_LPAR = r'\('
t_LT = r'<'
t_LTE = r'\<\='
t_MIN = r'-'
t_MULT = r'\*'
t_NEQU = r'\!\='
t_PLUS = r'\+'
t_RPAR = r'\)'
t_SEMI = r';'
t_ignore_COMM = r'(\$(?s).*\$)'  # comment syntax: $ ... $
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


# ############################ PARSER ############################# #
precedence = (
    ('left', 'PLUS', 'MIN'),
    ('left', 'MULT', 'DIV'),
    # ('right','UMINUS'),
)

st = {}


def p_program(p):
    """
    program : statements
    """
    print("", end='')


def p_statements(p):
    """
    statements : statement
               | statements statement
    """
    print("", end='')


def p_statement(p):
    """
    statement : attribution SEMI
              | if SEMI
              | if_else SEMI
              | expression SEMI
              | var_declaration SEMI
              | var_declaration_attribution SEMI
              | while SEMI
              | write SEMI
              | writeln SEMI
    """
    print("", end='')


def p_attribution(p):
    """
    attribution : IDEN EQU expression
    """
    if p[1] in st:
        st[p[1]][1] = p[3]
    else:
        exit(f"Name {p[1]} not defined")


def p_if(p):
    """
    if : IF LPAR rel_expression RPAR THEN BEGIN statements END
    """
    if p[3]:
        p[0] = p[7]
    else:
        p[0] = 0


def p_if_else(p):
    """
    if_else : IF LPAR rel_expression RPAR THEN BEGIN statements END ELSE BEGIN statements END
    """
    if p[3]:
        p[0] = p[7]
    else:
        p[0] = p[11]


def p_expression(p):
    """
    expression : term
               | term PLUS term
               | term MIN term
               | term OR term
    """
    if len(p) > 2:

        if p[2] == '+':
            p[0] = p[1] + p[3]

        elif p[2] == '-':
            p[0] = p[1] - p[3]

        elif p[2] == 'or':
            p[0] = p[1] | p[3]

    else:

        p[0] = p[1]


def p_var_declaration(p):
    """
    var_declaration : type IDEN
    """
    st[p[2]] = [p[1], None]


def p_var_declaration_attribution(p):
    """
    var_declaration_attribution : type IDEN EQU expression
    """
    st[p[2]] = [p[1], p[4]]


def p_while(p):
    """
    while : WHILE LPAR rel_expression RPAR DO BEGIN statements END
    """
    pass


def p_write(p):
    """
    write : WRITE LPAR expression RPAR
    """
    print(p[3], end='')


def p_writeln(p):
    """
    writeln : WRITELN LPAR expression RPAR
    """
    print(p[3])


def p_rel_expression(p):
    """
    rel_expression : expression LT expression
                   | expression LTE expression
                   | expression GT expression
                   | expression GTE expression
                   | expression DEQU expression
                   | expression NEQU expression
    """
    if p[2] == '<':
        p[0] = p[1] < p[3]

    elif p[2] == '<=':
        p[0] = p[1] <= p[3]

    elif p[2] == '>':
        p[0] = p[1] > p[3]

    elif p[2] == '>=':
        p[0] = p[1] >= p[3]

    elif p[2] == '==':
        p[0] = p[1] == p[3]

    elif p[2] == '!=':
        p[0] = p[1] != p[3]


def p_term(p):
    """
    term : factor
         | factor MULT factor
         | factor DIV factor
         | factor AND factor
    """
    if len(p) > 2:

        if p[2] == '*':
            p[0] = p[1] + p[3]

        elif p[2] == '/':
            p[0] = p[1] // p[3]

        elif p[2] == 'and':
            p[0] = p[1] & p[3]

    else:

        p[0] = p[1]


def p_factor(p):
    """
    factor : NUMB
           | IDEN
           | LPAR expression RPAR
    """
    if len(p) > 2:

        p[0] = p[2]

    else:
        try:
            int(p[1])
            p[0] = p[1]
        except ValueError:
            if p[1] in st:
                p[0] = st[p[1]][1]
            else:
                exit(f"Name {p[1]} not defined")


def p_type(p):
    """
    type : INTEGER
    """
    p[0] = p[1]


def p_error(p):
    ptype = p.type
    pvalue = p.value if ptype == "IDEN" else ''
    exit(f"Syntax error at {ptype} {pvalue}")


parser = yacc.yacc()

with open('test.pas', 'r') as f:

    program = f.read()

    print(program)
    print("\n--------------------\n")

    parser.parse(program)
