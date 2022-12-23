# 문자 유형 (charClass 값)

LETTER = 0
DIGIT = 1
UNKNOWN = 99


# 토큰 코드 (nextToken 값)
INT_LIT = 10
IDENT = 11
LEFT_BRACE = 12
RIGHT_BRACE = 13
SEMI = 14
COMMA = 15
EOF = 15
ERROR = -1

class AR(object):
    def __init__(self, RA, DL, *LV):
        self.ARI = []
        self.ARI.append(RA, DL)
        for vari in LV:
            self.ARI.append(vari)



# 어휘 분석용 클래스
class Token(object):
    def __init__(self, program):
        self.charClass = -1
        self.token_string = ""
        self.nextChar = ""
        self.nextToken = 0
        self.program = program
        self.index = 0
        self.length = 0
        self.token = 0

        self.switch_lexical_case = {  # 문자 유형에 따른 함수 매칭
        LETTER : self.letter,
        DIGIT : self.digit,
        UNKNOWN : self.unknown,
        EOF : self.eof
        }

    def switch_func(self, x): # 토큰 분류용 switch 결과 반환 함수
        return {
            '{' : LEFT_BRACE,
            '}' : RIGHT_BRACE,
            ',' : COMMA,
            ';' : SEMI,
            '$' : EOF,
        }.get(x, SEMI)

    def lookup(self, ch): # 연산자, 괄호 조사 후 그 토큰 반환 함수
        self.addChar()
        self.nextToken = self.switch_func(ch)
        if (self.nextToken == ASSIGN_OP): # ':=' 지정
            self.nextChar = self.program[self.index]
            self.index += 1
            self.addChar()
        return self.nextToken

    def addChar(self):
        self.token_string += self.nextChar
        self.lexLen += 1
    
    def getChar(self): # 입력으로부터 다음 번째 문자를 가져옴, 그 문자 유형 결정 함수
        self.nextChar = self.program[self.index]
        self.index += 1
        if ( self.nextChar!= "$"):
            if (self.nextChar.isalpha()):
                self.charClass = LETTER
            elif (self.nextChar.isdigit()):
                self.charClass = DIGIT
            else:
                self.charClass = UNKNOWN
        else:
            self.charClass = EOF
    
    def getNonBlank(self): # white-space를 반환할 때까지 getchar 호출 함수
        while (self.nextChar <= " "):
            self.getChar()

    def letter(self):
        self.addChar()
        self.getChar()
        while(self.charClass == LETTER or self.charClass == DIGIT):
            self.addChar()
            self.getChar()
        self.nextToken = IDENT

    def digit(self):
        self.addChar()
        self.getChar()
        while(self.charClass == DIGIT):
            self.addChar()
            self.getChar()
        self.nextToken = INT_LIT

    def unknown(self):
        self.lookup(self.nextChar)
        self.getChar()

    def eof(self):
        self.nextToken = EOF
        self.token_string = "EOF"

    def lexical(self):
        self.lexLen = 0
        self.token_string = ""
        self.getNonBlank()
        self.switch_lexical_case[self.charClass]()
        return self.nextToken, self.token_string