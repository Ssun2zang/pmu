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
EOF = -1


class Token(object):
    def __init__(self, program):
        self.charClass = -1
        self.token_string = ""
        self.nextChar = ""
        self.nextToken = 0
        self.program = program
        self.index = 0
        self.length = len(self.program)
        self.token = 0