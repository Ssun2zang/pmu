import sys

global charClass
global lexeme
global nextChar
global lexLen
global token
global nextToken

LETTER = 0
DIGIT = 1
UNKNOWN = 99

INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
EOP = -1

def switch_func(x):
    return {
        '(' : LEFT_PAREN,
        ')' : RIGHT_PAREN,
        '+' : ADD_OP,
        '-' : SUB_OP,
        '*' : MULT_OP,
        '/' : DIV_OP,
    }.get(x, EOP)

def lookup(ch):
    addChar()
    nextToken = switch_func(ch)
    return nextToken

def addChar():
    lexeme += nextChar
    pass

def getChar():
    pass

def getNonBlank():
    pass

def lexical():
    pass


def main():
    strings = []
    file = open(sys.argv[1], "r")
    while True:
        line = file.readline()
        if not line:
            break
        strings.append(line.strip())
    file.close()    
    program = " ".join(strings)
    print(program)



if __name__ == "__main__":
    main()





