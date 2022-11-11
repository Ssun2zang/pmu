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
        }.get(x, 1213)

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
            ERROR : "OK",
        }
        self.symbol_table = { }
    
    def checkFollow(self, ident):
        if (ident not in self.symbol_table):
            print("ERROR")
            return 0
        return 1
    
    def assignident(self, ident, val):
        self.symbol_table[ident] = val

    def cnt_stmt_anly(self, type):
        self.stmt_anly[type] += 1

    def getval(self, ident):
        if (self.checkFollow(ident)):
            return self.symbol_table[ident]

    def reset(self):
        self.stmt_anly = {
            'ID' : 0,
            'CONST' : 0,
            'OP' : 0,
            'ERROR' : "OK",
        }

    
class Parser(object):
    def __init__(self, program):
        self.T = Token(program)
        self.G = Grammar()
        self._stmt = ""
        pass

    def prog(self):
        self.stmts()

    def stmts(self): # <stmts> -> <stmt> | <stmt><semi><stmts>
        self.stmt()
        if (self.T.nextToken == SEMI):
            self.T.lexical()
            self.stmts()
        

    def stmt(self): # <stmt> -> <ident><assign_op><expr>
        self.G.reset()
        self._stmt = ""
        if (self.T.nextToken == IDENT):
            ident_name = self.T.token_string
            self.G.cnt_stmt_anly('ID')
            self._stmt += self.T.nextToken
            self.T.lexical()
            if (self.T.nextToken == ASSIGN_OP):
                    self._stmt += self.T.nextToken
                    self.T.lexical()
            else:
                print("오류 발생") # 수정
                return
            val = self.expr()
            self.G.assignident(ident_name, val)
            # print(self.G.symbol_table)
            print(self._stmt)
            print(self.G.stmt_anly)
        else:
            print("오류발생")

    def expr(self): # <expr> -> <term><term_tail>
        # print("ex시작")
        val = self.term() # parse first term
        if (self.T.nextToken == ADD_OP or self.T.nextToken == SUB_OP):
            rval, isadd = self.term_tail()
            if (isadd):
                val += rval
            else:
                val -= rval
        # print("ex끝")
        return val


    def term(self): # <term> -> <factor><factor_tail>
        val = self.factor()
        if (self.T.nextToken == MULT_OP or self.T.nextToken == DIV_OP):
            rval, ismult = self.factor_tail()
            if (ismult):
                val *= rval
            else:
                val /= rval
        # print("term끝")
        return val

    def factor(self): # <factor> -> <left_paren><expr><rigth_paren> | <ident> | <const>
        # print("factor시작")
        if (self.T.nextToken == IDENT):
            self.G.cnt_stmt_anly('ID')
            rval = self.T.token_string
            self._stmt += self.T.nextToken
            self.T.lexical()
            val = self.G.getval(rval)
            return val
        elif(self.T.nextToken == INT_LIT):
            self.G.cnt_stmt_anly('CONST')
            rval = self.T.token_string
            self._stmt += self.T.nextToken
            self.T.lexical()
            return int(rval)
        else:
            if (self.T.nextToken == LEFT_PAREN):
                self._stmt += self.T.nextToken
                self.T.lexical()
                val = self.expr()
                if (self.T.nextToken == RIGHT_PAREN):
                    self._stmt += self.T.nextToken
                    self.T.lexical()
                    return val
                else:
                    print(self.T.nextToken)
                    print("오류 발생") # 수정
                    return
            else:
                print(self.T.nextToken)
                print("오류발생")
                return

    def term_tail(self):
        if (self.T.nextToken == ADD_OP or self.T.nextToken == SUB_OP):
            self.G.cnt_stmt_anly('OP')
            isadd = self.add_op()
            val = self.term()
            rval = 0
            if (self.T.nextToken == ADD_OP or self.T.nextToken == SUB_OP):
                rval, isadd = self.term_tail()
            if(isadd):
                val += rval
            else:
                val -= rval
            return val, isadd
        
        

    def factor_tail(self):
        if (self.T.nextToken == MULT_OP or self.T.nextToken == DIV_OP):
            self.G.cnt_stmt_anly('OP')
            ismult = self.mult_op()
            val = self.factor()
            rval = 1
            if (self.T.nextToken == MULT_OP or self.T.nextToken == DIV_OP):
                rval, ismult = self.factor_tail()
            if(ismult):
                val *= rval
            else:
                val /= rval
            return val, ismult

    def add_op(self):
        token = self.T.nextToken
        self._stmt += self.T.nextToken
        self.T.lexical()
        if (token == ADD_OP):
            return 1
        else:
            return 0

    def mult_op(self):
        token = self.T.nextToken
        self._stmt += self.T.nextToken
        self.T.lexical()
        if (token == MULT_OP):
            return 1
        else:
            return 0

            

