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
EOF = 16
ERROR = -1

# 에약어

PRINT_ARI = 30
CALL = 31
VARIABLE = 32




# class AR(object):
#     def __init__(self, Fname, RA, DL):
#         self.ARI = []
#         self.Fname = Fname
#         self.ARI.append(RA)
#         self.ARI.append(DL)
#         self.top = 1

#     def addvar(self, *LV):
#         for vari in LV:
#             self.ARI.append(vari)
#             self.top +=1

#     def printari(self):
#         print(self.Fname+":", end = " ")
#         for i in range(1, len(self.top)-1):
#             print("Local variable: " + self.ARI[-i])
#         if (self.Fname != "main"):
#             print("Dynamic Link: " + self.ARI[1])
#             print("Return Address: " + self.ARI[0][0] + ": " + self.ARI[0][1])

#     def getfname(self):
#         return self.Fname
    

class RTstack(object):
    def __init__(self):
        self.stack=[]
        self.fnamelist = {}
        self.EP = 0
        self.line = 0
        self.top = 0

    def AR(self, Fname, RA, DL):
        self.stack.append(RA)
        self.stack.append(DL)
        self.EP = self.top
        self.top+=2
        self.fnamelist[self.EP] = Fname

    def addvar(self, *LV):
        for vari in LV:
            self.stack.append(vari)
            self.top +=1

    def printari(self):
        rslist = self.fnamelist.keys()
        rslist.sort()
        start = rslist.pop()
        end = self.top
        while (rslist):
            for i in reversed(range(start, end+1)):
                if (i-start == 1):
                    print("Dynamic Link: " + self.stack[i])
                elif (i == start):
                    print("Return Address: " + self.stack[i])
                else:
                    print("Local variable: " + self.stack[i])
            end = start -1
            start = rslist.pop()

    def callf(self, fname):
        ARI = self.AR(fname, [self.EP, self.line], self.EP)
        EP +=1
        self.stack.append(ARI)

    def printref(self, ident):
        temp_s = self.EP
        temp_e = self.EP + self.stack[self.EP]
        while (temp_s>0):
            pass
            # for i in range 

        pass

    def readf(self):
        pass



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