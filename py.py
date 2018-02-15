import os,sys

### parser

import ply.lex as lex

tokens = ['ID']

t_ignore = ' \t\r\n'
t_ignore_COMMENT = '\#.*'

def t_ID(t):
    r'[a-zA-Z0-9_]+'
    return t

def t_error(t): raise SyntaxError(t)

lex.lex()
lex.input(sys.stdin.read())

while True:
    W[lex.token().value]()
