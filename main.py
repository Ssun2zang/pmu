import sys
from Parsing import *

def main():
    program = make_string(sys.argv[1])
    T = Token(program)
    T.length = len(program)
    T.getChar()

    while(True):
        T.lexical()
        if (T.nextToken == EOF):
            break


if __name__ == "__main__":
    main()