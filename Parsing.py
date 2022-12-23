# 문자 유형 (charClass 값)

LETTER = 0
DIGIT = 1
UNKNOWN = 99

# 토큰 코드 (nextToken 값)
INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
SEMI = 27
EOF = 28
ERROR = -1

# 문법에 사용
PROG = 30
S = 31
ST = 32
E = 33
T = 34
F = 35
T_T = 36
F_T = 37


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
            '(' : LEFT_PAREN,
            ')' : RIGHT_PAREN,
            '+' : ADD_OP,
            '-' : SUB_OP,
            '*' : MULT_OP,
            '/' : DIV_OP,
            ':' : ASSIGN_OP,
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
            if (self.nextChar.isalpha() or self.nextChar == "_"):
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
        # print("Next token is {}, Next lexeme is {}".format(self.nextToken, self.token_string))
        return self.nextToken, self.token_string
    
    
def make_string(filename):
    strings = []
    file = open(filename, "r")
    while True:
        line = file.readline()
        if not line:
            break
        strings.append(line.strip())
    file.close() 
    program = " ".join(strings)  # 프로그램 만들기
    program += "$"
    return program


class Grammar(object):
    def __init__(self):
        self.stmt_anly = {
            'ID' : 0,
            'CONST' : 0,
            'OP' : 0,
            'ERROR' : "OK", # 에러 메시지 저장
        }

        self.error_table = { # 관리 에러 목록
            1 : "중복 연산자",
            2 : "정의되지 않은 변수 참조",
            3 : "잘못된 연산자 사용",
            4 : ":= 추가",
            5 : ") 추가"
        }
        self.symbol_table = { } # ident 값 저장
    
    def checkFollow(self, ident): # symbol_table에 정의되었는지 확인
        if (ident not in self.symbol_table):
            return 0
        return 1
    
    def assignident(self, ident, val): # symbol_table에 변수-value 추가
        self.symbol_table[ident] = val

    def cnt_stmt_anly(self, type): # id, const, op 1 추가
        self.stmt_anly[type] += 1

    def getval(self, ident): # symbol_table에 정의된 변수 값 가져오기, 정의되지 않은 경우 Unknown 값으로 저장 및 리턴
        if (self.checkFollow(ident)):
            return self.symbol_table[ident]
        else:
            self.stmt_anly['ERROR'] = "(Error)\"정의되지 않은 변수({})가 참조됨\"".format(ident)
            self.assignident(ident, "Unknown")
            return "Unknown"

    def reset(self): # stmt가 바뀔 때 reset
        self.stmt_anly = {
            'ID' : 0,
            'CONST' : 0,
            'OP' : 0,
            'ERROR' : "(OK)",
        }

    def printST(self):
        print(self.symbol_table)

    
class Parser(object):
    def __init__(self, program):
        self.T = Token(program)
        self.G = Grammar()
        self._stmt = ""  # stmt 내용 저장

    def prog(self): # <prog> -> <stmts>
        self.stmts()
        print("Result==>", end=' ')
        for key, value in self.G.symbol_table.items():
            print("{}:{};".format(key, value), end=" ")

    def stmts(self): # <stmts> -> <stmt> | <stmt><semi><stmts>
        self.stmt()
        if (self.T.nextToken == SEMI):
            self.T.lexical()
            self.stmts()
        

    def stmt(self): # <stmt> -> <ident><assign_op><expr>
        self.G.reset()
        try: 
            self._stmt = ""
            if (self.T.nextToken == IDENT):
                ident_name = self.T.token_string
                self.G.cnt_stmt_anly('ID')
                self._stmt += self.T.token_string
                self.T.lexical()
                if (self.T.nextToken == ASSIGN_OP):
                        self._stmt += self.T.token_string
                        self.T.lexical()
                else:
                    self.G.stmt_anly['ERROR'] = "(Warning)\":= 기호 추가\""
                    self._stmt += ":="
                val = self.expr()
                self.G.assignident(ident_name, val)
        except:
            self.G.stmt_anly['ERROR'] = "(Error) 수정할 수 없는 에러 발생"
            if (ident_name):
                self.G.assignident(ident_name, "Unknown")
        finally:
            self._stmt += ";"
            print(self._stmt)
            print("ID: {}; CONST: {}; OP: {};".format(self.G.stmt_anly['ID'], self.G.stmt_anly['CONST'], self.G.stmt_anly['OP']))
            print(self.G.stmt_anly['ERROR'])

    def expr(self): # <expr> -> <term><term_tail>
        val = self.term()
        if (self.T.nextToken == ADD_OP or self.T.nextToken == SUB_OP):
            rval, isadd = self.term_tail()
            if (val == "Unknown" or rval == "Unknown"): # 에러 처리
                return "Unknown"
            if (isadd):
                val += rval
            else:
                val -= rval
        if (val == "Unknown"): # 에러 처리
            return "Unknown"
        # print("ex끝")
        return val


    def term(self): # <term> -> <factor><factor_tail>
        val = self.factor()

        if (self.T.nextToken == MULT_OP or self.T.nextToken == DIV_OP):
            rval, ismult = self.factor_tail()
            if (val == "Unknown" or rval == "Unknown"): # 에러 처리
                return "Unknown"
            if (ismult):
                val *= rval
            else:
                val /= rval
        if (val == "Unknown"): # 에러 처리
            return "Unknown"
        return val

    def factor(self): # <factor> -> <left_paren><expr><rigth_paren> | <ident> | <const>
        if (self.T.nextToken == IDENT): # <ident>
            self.G.cnt_stmt_anly('ID')
            rval = self.T.token_string
            self._stmt += self.T.token_string
            self.T.lexical()
            val = self.G.getval(rval)
            return val
        elif(self.T.nextToken == INT_LIT): # <const>
            self.G.cnt_stmt_anly('CONST')
            rval = self.T.token_string
            self._stmt += self.T.token_string
            self.T.lexical()
            return int(rval)
        else:
            if (self.T.nextToken == LEFT_PAREN): # <left_paren><expr><rigth_paren>
                self._stmt += self.T.token_string
                self.T.lexical()
                val = self.expr()
                if (self.T.nextToken == RIGHT_PAREN):
                    self._stmt += self.T.token_string
                    self.T.lexical()
                    return val
                else:
                    self.G.stmt_anly['ERROR'] = "(Warning)\") 기호 추가\""
                    self._stmt += ")"
                    return
            else:
                while(self.T.nextToken not in [IDENT, INT_LIT, LEFT_PAREN, SEMI]):
                    self.G.stmt_anly['ERROR'] = "(Warning)\"잘못된 연산 형식으로 다음 연산자 제거\"".format(self._stmt[-1])
                    self.T.lexical()
                return

    def term_tail(self): # <term_tail> -> <add_op><term><term_tail> | E
        if (self.T.nextToken == ADD_OP or self.T.nextToken == SUB_OP):
            self.G.cnt_stmt_anly('OP')
            isadd = self.add_op()
            if (self.T.nextToken not in [IDENT, INT_LIT, LEFT_PAREN]):
                if (self.T.token_string == self._stmt[-1]): # 중복 연산자 삭제
                    self.G.stmt_anly['ERROR'] = "(Warning)\"중복 연산자({}) 제거\"".format(self._stmt[-1])

                    while(self.T.token_string == self._stmt[-1]):
                        self.T.lexical()
                while(self.T.nextToken not in [IDENT, INT_LIT, LEFT_PAREN, SEMI]):
                    self.G.stmt_anly['ERROR'] = "(Warning)\"잘못된 연산 형식으로 다음 연산자 제거\"".format(self._stmt[-1])
                    self.T.lexical()
            val = self.term()
            rval = 0
            if (self.T.nextToken == ADD_OP or self.T.nextToken == SUB_OP):
                rval, isadd = self.term_tail()
            
            if (val == "Unknown" or rval == "Unknown"): # 에러 처리
                return "Unknown", isadd
            if(isadd):
                val += rval
            else:
                val -= rval
            return val, isadd

    def factor_tail(self): # <factor_tail> -> <mult_op><factor><factor_tail> | E
        if (self.T.nextToken == MULT_OP or self.T.nextToken == DIV_OP):
            self.G.cnt_stmt_anly('OP')
            ismult = self.mult_op()
            if (self.T.nextToken not in [IDENT, INT_LIT, LEFT_PAREN]):
                if (self.T.token_string == self._stmt[-1]): # 중복 연산자 삭제
                    self.G.stmt_anly['ERROR'] = "(Warning)\"중복 연산자({}) 제거\"".format(self._stmt[-1])
                    while(self.T.token_string == self._stmt[-1]):
                        self.T.lexical()
                while(self.T.nextToken not in [IDENT, INT_LIT, LEFT_PAREN]):
                    self.G.stmt_anly['ERROR'] = "(Warning)\"잘못된 연산 형식으로 다음 연산자 제거\"".format(self._stmt[-1])
                    self.T.lexical()
            
            val = self.factor()
            rval = 1
            if (self.T.nextToken == MULT_OP or self.T.nextToken == DIV_OP):
                rval, ismult = self.factor_tail()

            if (val == "Unknown" or rval == "Unknown"): # 에러 처리
                return "Unknown", ismult

            if(ismult):
                val *= rval
            else:
                val /= rval
            return val, ismult

    def add_op(self): # <add_op> -> + | -
        token = self.T.nextToken
        self._stmt += self.T.token_string
        self.T.lexical()
        if (token == ADD_OP):
            return 1
        else:
            return 0

    def mult_op(self): # <mult_op> -> * | /
        token = self.T.nextToken
        self._stmt += self.T.token_string
        self.T.lexical()
        if (token == MULT_OP):
            return 1
        else:
            return 0 

