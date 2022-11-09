import sys

# 전역 변수 선언
global charClass
global token_string
global nextChar
global lexLen
global token
global nextToken
global program
global index

# 문자 유형
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# 토큰 코드
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

def switch_func(x): # 토큰 분류용 switch 결과 반환 함수
    return {
        '(' : LEFT_PAREN,
        ')' : RIGHT_PAREN,
        '+' : ADD_OP,
        '-' : SUB_OP,
        '*' : MULT_OP,
        '/' : DIV_OP,
    }.get(x, EOF)

def lookup(ch): # 연산자, 괄호 조사 후 그 토큰 반환 함수
    addChar()
    global nextToken
    nextToken = switch_func(ch)
    return nextToken

def addChar():
    global token_string
    global nextChar
    token_string += nextChar
    pass

def getChar(): # 입력으로부터 다음 번째 문자를 가져옴, 그 문자 유형 결정 함수
    global index
    global nextChar
    global program
    global charClass
    nextChar = program[index]
    index += 1
    if ( nextChar!= EOF):
        if (nextChar.isalpha()):
            charClass = LETTER
        elif (nextChar.isdigit()):
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = UNKNOWN

    pass

def getNonBlank(): # white-space를 반환할 때까지 getchar 호출 함수
    global nextChar
    while (nextChar > " "):
        getChar()
    pass

def letter():
    global charClass
    global nextToken
    addChar()
    getChar()
    while(charClass == LETTER or charClass == DIGIT):
        addChar()
        getChar()
    nextToken = IDENT

def digit():
    global charClass
    global nextToken
    addChar()
    getChar()
    while(charClass == DIGIT):
        addChar()
        getChar()
    nextToken = INT_LIT

def unknown():
    lookup(nextChar)
    getChar()

def eof():
    global nextToken
    global token_string
    nextToken = EOF
    token_string = "EOF"

switch_lexical_case = {
    LETTER : letter,
    DIGIT : digit,
    UNKNOWN : unknown,
    EOF : eof
}

def lexical():
    global lexLen
    lexLen = 0
    getNonBlank()
    switch_lexical_case[charClass]()
    print("Next token is {}, Next lexeme is {}".format(nextToken, token_string))
    return nextToken


def main():
    strings = []
    file = open(sys.argv[1], "r")
    while True:
        line = file.readline()
        if not line:
            break
        strings.append(line.strip())
    file.close()    
    global program 
    program = " ".join(strings)
    global index
    index = 0
    print(program)
    # program = " ".join("(sum + 47) / total")
    getChar()
    global nextToken
    global token_string
    nextToken = 0  # 이거 맞나
    token_string = ""  # 이거 맞나
    while (nextToken != EOF):
        lexical()




if __name__ == "__main__":
    main()





