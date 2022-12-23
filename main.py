import sys
from Programming import *

def main():
    program = make_string(sys.argv[1])
    P = Parser(program)
    P.T.length = len(program)
    P.T.getChar()
    P.T.lexical()
    P.start()

if __name__ == "__main__":
    main()