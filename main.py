import sys
from Parsing import *

# python main.py eval1.txt

# def main():
#     program = make_string(sys.argv[1])
#     T = Token(program)
#     T.length = len(program)
#     T.getChar()

#     while(True):
#         T.lexical()
#         if (T.nextToken == EOF):
#             break

def main():
    program = make_string(sys.argv[1])
    P = Parser(program)
    P.T.length = len(program)
    P.T.getChar()
    P.T.lexical()
    P.prog()

if __name__ == "__main__":
    main()