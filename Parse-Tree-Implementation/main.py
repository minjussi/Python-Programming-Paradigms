# 1. Tokenizer: 입력받은 문자열을 토큰으로 나눔
def Tokenizer(input):
    tokens = []
    i = 0
    while (i < len(input)):
        # 괄호
        if (input[i] == "(" or input[i] == ")"):
            tokens.append(input[i])
            i += 1
            continue
        # 연산자
        if (input[i] in ["+", "-", "*", "/", "^"]):
            tokens.append(input[i])
            i += 1
            continue
        # 숫자
        if (input[i].isdigit()):
            num = ""
            while (i < len(input) and input[i].isdigit()):
                num += input[i]
                i += 1
            tokens.append(num)
            continue
        # 문자
        if (input[i].isalpha()):
            string = ""
            while (i < len(input) and input[i].isalpha()):
                string += input[i]
                i += 1
            tokens.append(string)
            continue
        # 공백
        if (input[i].isspace()):
            i += 1
            continue
    return tokens

# 2. Parser: 토큰을 활용해 recursive descent parser 구현
# 에러는 전부 raise로 처리하고, 나중에 try-except로 처리
# op의 우선순위는 ^ > *, / > +, -
# 따라서 가장 마지막에 계산되는 expr에서 +, - 다루고,
# term에서 *, / 다루고,
# power에서 ^ 다루고,
# 괄호와 상수는 factor에서 다룸 (unary minus까지)
class Parser:
    # 공통으로 관리할 tokens와 index
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
    
    # parser가 처음으로 실행되는 곳이자 최종 결과 반환
    def parse(self):
        start_parse = self.expr()
        # index와 token 개수는 같아져야 함
        if self.idx != len(self.tokens)-1:
            raise
        # 정상적이면 parse tree 반환
        return start_parse
    
    # +와 - 연산자
    def expr(self):
        #print("enter e")
        left = self.term()
        if (self.idx >= len(self.tokens) or self.tokens[self.idx] is None):
            raise
        while (self.tokens[self.idx] is not None and self.tokens[self.idx] in ["+", "-"]):
            op = self.tokens[self.idx]
            if (self.idx < len(self.tokens)-1):
                self.idx += 1
            right = self.term()
            left = (op, left, right)
        #print("return e", left)
        return left
    
    # *와 / 연산자
    def term(self):
        #print("enter t")
        left = self.power()
        if (self.idx >= len(self.tokens) or self.tokens[self.idx] is None):
            raise
        while (self.tokens[self.idx] is not None and self.tokens[self.idx] in ["*", "/"]):
            op = self.tokens[self.idx]
            if (self.idx < len(self.tokens)-1):
                self.idx += 1
            right = self.power()
            left = (op, left, right)
        #print("return t", left)
        return left
    
    # ^ 연산자 (right associativity)
    def power(self):
        #print("enter p")
        left = self.factor()
        if (self.idx >= len(self.tokens) or self.tokens[self.idx] is None):
            raise
        while (self.tokens[self.idx] is not None and self.tokens[self.idx] == "^"):
            op = self.tokens[self.idx]
            if (self.idx < len(self.tokens)-1):
                self.idx += 1
            right = self.power()
            left = (op, left, right)
        #print("return p", left)
        return left
    
    # 괄호, 상수, unary minus
    def factor(self):
        #print("enter f")
        id = self.tokens[self.idx]
        # 정수값인 경우
        if (id.isdecimal()):
            # idx 한 개 올리고 정수값 반환
            if (self.idx < len(self.tokens)-1):
                self.idx += 1
            value = int(id)
            #print("return f", value)
            return value
        # 괄호인 경우 -> expr부터 새롭게 다시 시작해야함     
        elif (id == "("):
            if (self.idx < len(self.tokens)-1):
                    self.idx += 1
            new = self.expr()
            # self.idx 범위 확인
            if (self.idx >= len(self.tokens)):
                raise
            # 오른쪽 괄호 없으면 error
            if (self.tokens[self.idx] != ")"):
                raise
            # 오른쪽 괄호가 있으면 일단 index를 1 증가시킴
            else:
                self.idx += 1  
            #print("return f", new)
            return new
        # unary minus -> 오른쪽에만 식 존재 (right associativity)
        elif (id == "-"):
            self.idx += 1
            if (self.idx > len(self.tokens) or self.tokens[self.idx] is None):
                raise
            unary = self.factor()
            unary = ("neg", unary)
            #print("return f", unary)
            return unary
        else:
            raise

# 3. Calculator: 파싱된 식을 활용해 left->right 순서로 계산  
def Calculator(parsed):
    # 정수값(튜플이 아닐 때)이면 그냥 반환
    if (isinstance(parsed, int)):
        return parsed
    
    # 튜플형태로 되어 있으면 계산 (recursive)
    else:
        if (parsed[0] == "+"):
            left = Calculator(parsed[1])
            right = Calculator(parsed[2])
            return left+right
        
        elif (parsed[0] == "-"):
            left = Calculator(parsed[1])
            right = Calculator(parsed[2])
            return left-right
        
        elif (parsed[0] == "*"):
            left = Calculator(parsed[1])
            right = Calculator(parsed[2])
            return left*right
        
        elif (parsed[0] == "/"):
            left = Calculator(parsed[1])
            right = Calculator(parsed[2])
            return left/right
        
        elif (parsed[0] == "^"):
            left = Calculator(parsed[1])
            right = Calculator(parsed[2])
            return left**right

        elif (parsed[0] == "neg"):
            right = Calculator(parsed[1])
            return -(right)

def run_from_file(input_file, result_file):
    with open(input_file, "r") as f_input, open(result_file, "w") as f_result:
        lines = f_input.readlines()
        # 개행 문자 제거
        lines = [line.strip() for line in lines]

        for i in lines:
            expression = i
            f_result.write(f"Expression: {expression}\n")
            # Tokenizer
            tokens = Tokenizer(expression)
            #print(tokens)
            f_result.write(f"Tokens: {tokens}\n")
            try:
                # Parser
                # raise 발생하면 -> exception으로 넘어가서 Error 적음
                parser = Parser(tokens)
                parse_tree = parser.parse()
                #print(parse_tree)
                f_result.write(f"Parse Tree: {parse_tree}\n")

                # Calculator
                # parser가 문제 없이 실행되면 calculator도 자연스럽게 실행됨
                result = Calculator(parse_tree)
                #print(result)
                f_result.write(f"Result: {result}\n")

            except Exception as e:
                #print("Error\n")
                f_result.write("Error\n")
            f_result.write("\n")
     
run_from_file("expressions.txt", "result.txt")