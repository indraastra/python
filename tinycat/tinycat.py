#!/usr/bin/python

import shlex
import sys

DEBUG = False
PROMPT = '$: '
OUTPUT = '-: '

### utility functions
def out(msg):
    print OUTPUT + msg

def exit(msg):
    print msg
    sys.exit(0)

def stringify(r):
    if isinstance(r, list):
        return '|' + ' '.join(stringify(i) for i in r) + '|'
    if isinstance(r, str):
        return '"' + str(r) + '"'
    else:
        return str(r)

def makePusher(t):
    def tmpfn(s):
        s.append(t)
    return tmpfn

def unquote(s):
    return s[1:-1]

### special functions
def dumpStack(s):
    return '[' + ' '.join(stringify(i) for i in s) + ']'

def clearStack(s):
    s[:] = []

### stack functions I couldn't write with lambdas
def tinycat_mapFn(stack):
    quotedFn = list(tokenize(unquote(stack.pop())))
    l = list(tokenize(unquote(stack.pop())))
    result = []
    for i in l:
        newstack = stack[:]
        commands = [i] + quotedFn
        results = list(execute(parse(commands), newstack))
        result.append(newstack[-1])
    stack.append(result)

### stack functions I _could_ write with lambdas
functions = {
        'add': (2, lambda s: s.append(s.pop() + s.pop())),
        'sub': (2, lambda s: s.append(s.pop() - s.pop())),
        'mult': (2, lambda s: s.append(s.pop() * s.pop())),
        'div': (2, lambda s: s.append(s.pop(-2) / s.pop())),
        'dup': (1, lambda s: s.append(s[-1])),
        'swap': (2, lambda s: s.extend([s.pop(), s.pop()])),
        'pop': (1, lambda s: s.pop() if len(s) > 0 else None),
        'eval': (1, lambda s: s.extend(map(str, evaluate(unquote(s.pop()), s)))),
        'car': (1, lambda s: s.append(s.pop()[0])),
        'cdr': (1, lambda s: s.append(s.pop()[1:])),
        'map': (2, tinycat_mapFn),
        ':peek': (None, lambda s: out(dumpStack(s))),
        ':clear': (None, clearStack),
        ':quit': (None, lambda s: exit('bye!')),
}
aliases = [('+', 'add'),
           ('*','mult'),
           ('-','sub'),
           ('/','div'),
           ('.','pop'),
           (':q',':quit'),
           (':p',':peek'),
           (':c',':clear')]
for l,r in aliases:
    functions[l] = functions[r]

### repl loop; gets input, then tokenizes and evaluates it
def repl():
    stack = []
    while True:
        try:
            text = raw_input(PROMPT)
        except EOFError:
            exit('bye!')
        results = evaluate(text, stack)
        if results:
            out(' '.join(results))
        if DEBUG:
            print ' ## results:', list(results)
        if DEBUG:
            print " ## stack:", dumpStack(stack)

### tokenizer; takes input string and uses shlex module to turn it into
### a token stream
def tokenize(text):
    if DEBUG:
        print ' ## text:', text
    lexer = shlex.shlex(text)
    lexer.wordchars += ".:"
    lexer.quotes += "|"
    try:
        for token in lexer:
            yield token
    except ValueError, err:
        out('LEXING ERROR: ' + lexer.error_leader() + ' ' + str(err))

### parser; converts token stream into a stream of (numargs, fn) pairs
### where `numargs` is the number of elements the function `fn` expects to be
### on the stack. this number is used for useful error messages.
def parse(tokens):
    try:
        for token in tokens:
            command = [token]
            if token in functions:
                command.extend(functions[token])
            elif token[0] == '"' or token[0] == "'":
                command.extend([0, lambda s: s.append(token[1:-1])])
            elif token[0] == '|':
                command.append(None)
                #subtokens = list(tokenize(text))
                command.append(makePusher(token))
            else:
                command.append(None)
                if '.' in token:
                    command.append(makePusher(float(token)))
                else:
                    command.append(makePusher(int(token)))
            yield command
    except ValueError, err:
        out('PARSING ERROR: invalid token ' + token)

### executor; takes the parser output stream and evaluates the functions in it,
### streaming out the results of evaluation when necessary
def execute(commands, stack):
    try:
        for c in commands:
            if DEBUG:
                print ' ## executing', c, 'on', dumpStack(stack)
            result = c[-1](stack)
            if result:
                yield stringify(result)
    except IndexError, err:
        out('STACK UNDERFLOW ERROR: ' + c[0] + ' requires ' + str(c[1]) + ' arguments on stack')
    except ValueError, err:
        out('RUNTIME ERROR: ' + c[0] + ' | ' + str(err))

### evaluator; accepts text and composes tokenizer, executor and parser to
### yield results directly.
def evaluate(text, stack):
    return list(execute(parse(tokenize(text)), stack))

if __name__ == "__main__":
    repl()
