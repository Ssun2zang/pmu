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
REF = 17
ERROR = -1

# 에약어

PRINT_ARI = 30
CALL = 31
VARIABLE = 32


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
    
# Run Time Stack
class RTstack(object):
    def __init__(self):
        self.stack=[]
        self.fnamelist = {}
        self.EP = 0
        self.line = 0
        self.top = 0

    def funcmain(self):
        self.fnamelist[0] = "main"

    def AR(self, Fname, RA, DL):
        self.stack.append(RA)
        self.stack.append(DL)
        self.EP = self.top
        self.top+=2
        self.fnamelist[self.EP] = Fname

    def addvar(self, vari):
        self.stack.append(vari)
        self.top +=1

    def printari(self):
        rslist = list(self.fnamelist.keys())
        rslist.sort()
        start = rslist.pop()
        end = self.top
        while (rslist):
            print(self.fnamelist[start], ": ", end="")
            for i in reversed(range(start, end)):
                if (i-start == 1):
                    print("Dynamic Link: " + str(self.stack[i]))
                elif (i == start):
                    print("Return Address: " + self.fnamelist[self.stack[i][0]]+ ": "+str(self.stack[i][1]))
                else:
                    print("Local variable: " + str(self.stack[i]))
                print("\t", end = " ")
            print(" ")
            end = start
            start = rslist.pop()
        print(self.fnamelist[start], ": ", end="")
        for i in reversed(range(start, end)):
            print("\tLocal variable: " + str(self.stack[i]))
        print(" ")


    def callf(self, fname, line):
        ARI = self.AR(fname, [self.EP, line], self.EP)

    def printref(self, ident):
        rslist = list(self.fnamelist.keys())
        rslist.sort()
        end = self.top
        loop = True
        linkcount = -1
        localoffset = 0
        while (rslist and loop):
            linkcount+=1
            start = rslist.pop()
            for i in range(start, end):
                
                if self.stack[i] == ident:
                    loop = False
                    localoffset = i-start
                    break
            end = start
        if (not loop):
            print(self.fnamelist[self.EP]+":"+ident+ " => " + str(linkcount) + ", " + str(localoffset))
            print("")




    def endAR(self):
        self.top = self.EP
        end = self.top-self.EP
        del self.fnamelist[self.EP]
        self.EP = self.stack[self.EP+1]
        for _ in range(0, end):
            self.stack.pop()




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
        if (self.token_string == "variable"):
            self.nextToken = VARIABLE
        elif (self.token_string == "call"):
            self.nextToken = CALL
        elif (self.token_string == "print_ari"):
            self.nextToken = PRINT_ARI
        else:
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


class Grammar(object):
    def __init__(self):
        self.func_anly = {}
        self.lineidx = 0
        self.varlist = []
    
    def func_var(self, vars): # 선언 변수 추가
        self.func_anly[self.lineidx] = vars  # [VARIABLE, x, y, z]
        self.lineidx +=1

    def func_call(self, funcname):
        self.func_anly[self.lineidx] = funcname  # [CALL, func1]
        self.lineidx +=1

    def func_printari(self):
        self.func_anly[self.lineidx] = [PRINT_ARI] # [PRINT_ARI]
        self.lineidx +=1

    def func_ref(self, x):
        self.func_anly[self.lineidx] = x # [REF, x]
        self.lineidx +=1
        
    def nameset(self, name): # function 이름 정보 추가
        self.func_anly["name"] = name

    def getline(self, idx): # 실행 중 사용
        return (self.func_anly[idx])

    def newfunc(self):
        self.func_anly.clear()
        self.lineidx = 0
        self.varlist.clear()

# 파서
class Parser(object):
    def __init__(self, program):
        self.T = Token(program)
        self.Glist = []
        self.G = Grammar()
        self._stmt = ""  # stmt 내용 저장
        self.fnamelist = []
        self.varnamelist = []
        self.reserved_word = ["variable", "call", "print_ari"]

    def start(self): # <start> -> <funcs>
        self.funcs()

    def funcs(self): # <funcs> -> <func> | <func><funcs>
        _G = Grammar()
        self.func(_G)
        if (self.T.nextToken == IDENT):
            self.funcs()
        self.Glist.append(_G)

    def func(self, G):
        fname = self.T.token_string
        if fname in self.fnamelist:  # 함수 정의할 때 이름 확인 (동일 이름 함수)
            print("Duplicate delcaration of the function name: "+ fname)
            quit()
        if fname in self.varnamelist:  # 함수 정의할 때 이름 확인 (동일 이름 변수)
            print("Duplicate declaration of the identifier or the function name : "+ fname)
            quit()
        if fname in self.reserved_word: # 함수 이름이 예약어와 같은지 확인
            print("Unable to save name as reserved word: "+fname)
            quit()
        G.nameset(fname)  
        self.fnamelist.append(fname)
        self.T.lexical()
        if (self.T.nextToken == LEFT_BRACE): # <func> -> <ident> {<func_body>}
            self.T.lexical()
            self.funcbody(G)
            if (self.T.nextToken == RIGHT_BRACE):
                self.T.lexical()
            else:
                print("Syntax Error.")
                quit()
        else:
            print("Syntax Error.")
            quit()
        
    def funcbody(self, G): # <func_body> -> <var_defs><stmts> | <stmts> 
        if(self.T.nextToken == VARIABLE):
            self.var_defs(G)
        self.stmts(G)

    def var_defs(self, G): # <var_defs> -> <var_def> | <var_def><var_defs>
        self.var_def(G)
        if (self.T.nextToken == VARIABLE):
            self.var_defs(G)
    
    def var_def(self, G): # <var_def> -> variable <var_list><semi>
        _varlist = [VARIABLE]
        self.T.lexical()
        self.var_list(_varlist, G)
        if (self.T.nextToken == SEMI):
            self.T.lexical()
        else:
            print("Syntax Error.")
            quit()
        G.func_var(_varlist)

    def var_list(self, _varlist, G): # <var_list> -> <ident> | <ident><comma><var_list>
        if (self.T.nextToken == IDENT): # <ident>
            if self.T.token_string in self.fnamelist:  # 변수 정의할 때 이름 확인 (동일 이름 함수)
                print("Duplicate declaration of the identifier or the function name : "+ self.T.token_string)
                print("")
                quit()
            if self.T.token_string in self.reserved_word: # 변수 이름이 예약어와 같은지 확인
                print("Unable to save name as reserved word: "+self.T.token_string)
                quit()

            if self.T.token_string in G.varlist: # 하나의 함수 내 같은 이름 지역 변수 확인
                print("Duplication declaration of the identifier: "+ self.T.token_string)
                print("")
                self.T.lexical()
            else:
                G.varlist.append(self.T.token_string)
                self.varnamelist.append(self.T.token_string)
                _varlist.append(self.T.token_string)
                self.T.lexical()
        
        
        if (self.T.nextToken == COMMA):
            self.T.lexical()
            self.var_list(_varlist, G)

    

    def stmts(self, G): # <stmts> -> <stmt> | <stmt><stmts>
        self.stmt(G)
        if (self.T.nextToken == CALL or self.T.nextToken == PRINT_ARI or self.T.nextToken == IDENT):
            self.stmts(G)
        

    def stmt(self, G): # <stmt> -> call <ident><semi> | print_ari <semi> | <ident><semi>
        if (self.T.nextToken == CALL):
            self.T.lexical()
            if (self.T.nextToken == IDENT): # <ident>
                G.func_call([CALL, self.T.token_string])
                self.T.lexical()
            if (self.T.nextToken == SEMI):
                self.T.lexical()
        elif (self.T.nextToken == PRINT_ARI):
            self.T.lexical()
            G.func_printari()
            if (self.T.nextToken == SEMI):
                self.T.lexical()
        elif (self.T.nextToken == IDENT):
            G.func_ref([REF, self.T.token_string])
            self.T.lexical()
            if (self.T.nextToken == SEMI):
                self.T.lexical()
        else:
            print("Syntax Error.")
            quit()

# run program
class runprogram(object):
    def __init__(self, Glist):
        self.Glist = Glist
        self.RTstack = RTstack()
    def run(self):
        print("Syntax O.K.")
        print("")
        self.RTstack.funcmain()
        now_func = {}
        find = False
        for func in self.Glist:
            if func.func_anly['name']=='main':
                now_func = func.func_anly
                find = True
                break
        if (find == False):  # main함수가 정의되지 않은경우 오류
            print("No starting function.")
            quit()
        for i in range(0, len(now_func)-1):
            keyword = now_func[i][0]
            if (keyword == VARIABLE):
                for j in range(1, len(now_func[i])):
                    self.RTstack.addvar(now_func[i][j])
            elif (keyword == CALL):
                self.funccall(now_func[i][1], i)
            elif (keyword == PRINT_ARI):
                self.RTstack.printari()
                pass
            else:
                self.RTstack.printref(now_func[i][1])
                pass

    def funccall(self, fname, line):
        self.RTstack.callf(fname, line)
        find = False
        for func in self.Glist:
            if func.func_anly['name']==fname:
                find = True
                now_func = func.func_anly
                break
        if (find == False):  # 정의되지 않은 함수 호출
            print("Call to undefined function: "+ fname)
            quit()
        for i in range(0, len(now_func)-1):
            keyword = now_func[i][0]
            if (keyword == VARIABLE):
                for j in range(1, len(now_func[i])):
                    self.RTstack.addvar(now_func[i][j])
            elif (keyword == CALL):
                self.funccall(now_func[i][1], i)
                pass
            elif (keyword == PRINT_ARI):
                self.RTstack.printari()
                pass
            else:
                self.RTstack.printref(now_func[i][1])
                pass # 호출
        self.RTstack.endAR()

        pass