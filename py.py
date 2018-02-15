import os,sys

### type system

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower() ; self.value = V
        self.nest = [] ; self.attr = {}
    def __lshift__(self,o): self.push(o)
    def push(self,o): self.nest.append(o) ; return self
    def pop(self): return self.nest.pop()
    def __setitem__(self,K,o): self.attr[K] = o ; return self
    def __getitem__(self,K): return self.attr[K]
    def __repr__(self): return self.dump()
    def head(self): return '<%s:%s>'%(self.type,self.value)
    def dump(self,depth=0,prefix=''):
        S = '\n'+'\t'*depth + prefix + self.head()
        for j in self.nest: S += j.dump(depth+1)
        return S

### primitives

class String(Object): pass

### composites

class Stack(Object): pass
class  Dict(Object): pass

### VM structures

D = Stack('DATA')
W = Dict('FORTH')   # root vocabulary

### core

def BYE(): sys.exit(0)

def ADD(): B = D.pop() ; A = D.pop() ; D.push(A+B)
W['+'] = ADD

### debug

def q(): print D
W['?'] = q
def qq(): print D ; print W ; BYE()
W['??'] = qq

### codegen

W['MODULE'] = 'FORTH'

### parser

import ply.lex as lex

tokens = ['ID','string']

states = (('string','exclusive'),)

t_ignore = ' \t\r\n'
t_ignore_COMMENT = '\#.*'

t_string_ignore = ''
def t_string(t):
    r'\''
    t.lexer.push_state('string')
    t.lexer.value = ''
def t_string_STR(t):
    r'\''
    t.lexer.pop_state()
    return String(t.lexer.value)
def t_string_char(t):
    r'.'
    t.lexer.value += t.value

def t_ID(t):
    r'[a-zA-Z0-9_?+]+'
    return t

def t_ANY_error(t): raise SyntaxError(t)

lex.lex()
lex.input(sys.stdin.read())

### compiler

def const(): WORD() ; N = D.pop().value ; W[N] = D.pop()
W['CONST'] = const

### interpreter

def WORD():
    token = lex.token()
    if not token: BYE()
    D << String(token.value)
    return token.type

def FIND():
    N = D.pop().value
    try: D << W[N]
    except KeyError: D << W[N.upper()]

def EXECUTE():
    E = D.pop()
    try: E()
    except TypeError: D.append(E)

def INTERPRET():
    while True:
        WORD() ; print D
#        if WORD() == 'ID':
#            FIND() ; EXECUTE()
#        print D
INTERPRET()

