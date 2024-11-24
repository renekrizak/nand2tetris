#Parses the tokenized jack code
"""
Rules:
class → 'class' className '{' classVarDec* subroutineDec* '}
classVarDec → ('static' | 'field') type varName (',' varName)* ';'
subroutineDec → ('constructor' | 'function' | 'method') ('void' | type) subroutineName
                '(' parameterList ')' subroutineBody
parameterList → ((type varName) (',' type varName)*)?
subroutineBody → '{' varDec* statements '}'
statements → statement*
statement → letStatement | ifStatement | whileStatement | doStatement | returnStatement
letStatement → 'let' varName ('[' expression ']')? '=' expression ';'
ifStatement → 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
whileStatement → 'while' '(' expression ')' '{' statements '}'
doStatement → 'do' subroutineCall ';'
returnStatement → 'return' expression? ';'
expression → term (op term)*
term → integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' 
      | subroutineCall | '(' expression ')' | unaryOp term
subroutineCall → subroutineName '(' expressionList ')'
                 | (className | varName) '.' subroutineName '(' expressionList ')'

"""


class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.current_token = tokens[0] if tokens else None

    def advance(self):
        #moves to the next token
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None
    
    def consume(self, expected_token_type=None, expected_token_value=None):
        if not self.current_token:
            raise SyntaxError("unexpected end of tokens")
        token_type, token_value = self.current_token

        if expected_token_type and token_type != expected_token_type:
            raise SyntaxError(f"Expected token type: {expected_token_type}, got {token_type}")
        if expected_token_value and token_value != expected_token_value:
            raise SyntaxError(f"Expected token value {expected_token_value}, got {token_value}")
        
        self.advance()

    def compileClass(self):
        """
class → 'class' className '{' classVarDec* subroutineDec* '}
        """

        # matches class keyword
        self.consume('keyword', 'class')

        # match className
        self.consume('identifier')

        #match { symbol
        self.consume('symbol', '{')

        while self.current_token and self.current_token[1] in ('static', 'field'):
            self.compileClassVarDec()
        
        while self.current_token and self.current_token[1] in ('constructor', 'function', 'method'):
            self.compileSubroutine()

        self.consume('symbol', '}')


    def compileClassVarDec(self):
        """
classVarDec → ('static' | 'field') type varName (',' varName)* ';'
        """
        self.consume('keyword', self.current_token[1])

        if self.current_token[0] == 'keyword' and self.current_token[1] in ('int', 'char', 'boolean'):
            self.consume('keyword')
        elif self.current_token[0] == 'identifier':
            self.consume('identifier')
        else:
            raise SyntaxError("Expected type ('int', 'char', 'boolean' or class name)")
    
        self.consume('identifier')

        while self.current_token and self.current_token == ('symbol', ','):
            self.consume('symbol', ',')
            self.consume('identifier')

        self.consume('symbol', ';')


    def compileSubroutine(self):
        """
        subroutineDec → ('constructor' | 'function' | 'method') ('void' | type) subroutineName
                '(' parameterList ')' subroutineBody
        """

        self.consume('keyword')

        if self.current_token[0] == 'keyword' and self.current_token[1] in ('void', 'int', 'char', 'boolean'):
            self.consume('keyword')
        elif self.current_token[0] == 'identifier':
            self.consume('identifier')
        else:
            raise SyntaxError("Expected void, primitive type or class type")

        self.consume('identifier')

        self.consume('symbol', '(')
        self.compileParameterList()
        self.consume('symbol', ')')

        self.consume('symbol', '{')        

        while self.current_token and self.current_token == ('keyword', 'var'):
            self.compileVarDec()

        self.compileStatements()
        self.consume('symbol', '}')

    def compileParameterList(self):
        
        if self.current_token and self.current_token[0] in ('keyword', 'identifier'):
            self.consume('keyword' if self.current_token[0] == 'keyword' else 'identifier')
            self.consume('identifier')

            while self.current_token and self.current_token == ('symbol', ','):
                self.consume('symbol', ',')
                self.consume('keyword' if self.current_token[0] == 'keyword' else 'identifier')
                self.consume('identifier')


    def compileSubroutineBody(self):
        """
            subroutineBody → '{' varDec* statements '}'
        """
        self.consume("symbol", "{")

        while self.current_token and self.current_token == ("keyword", 'var'):
            self.compileVarDec()

        self.compileStatements()

        self.consume('symbol', '}')

    def compileVarDec(self):
        """
        varDec → 'var' type varName (',' varName)* ';'
        """
        self.consume('keyword', 'var')

        if self.current_token[0] == 'keyword' and self.current_token[1] in ('int', 'char', 'boolean'):
            self.consume('keyword')
        elif self.current_token[0] == 'identifier':
            self.consume('identifier')
        else:
            raise SyntaxError("Expected types: int, char, boolean")
        
        self.consume('identifier')

        while self.current_token and self.current_token == ('symbol', ','):
            self.consume('symbol', ',')
            self.consume('identifier')

        self.consume('symbol', ';')

    def compileStatements(self):
        """
        statements → statement*
        statement → letStatement | ifStatement | whileStatement | doStatement | returnStatement
        """
        while self.current_token and self.current_token[0] == 'keyword' and self.current_token[1] in {'let', 'if', 'while', 'do', 'return'}:        
            if self.current_token == ('keyword', 'if'):
                self.compileIf()
            elif self.current_token == ('keyword', 'while'):
                self.compileWhile()
            elif self.current_token == ('keyword', 'let'):
                self.compileLet()
            elif self.current_token == ('keyword', 'do'):
                self.compileDo()
            elif self.current_token == ('keyword', 'return'):
                self.compileReturn()
            else: 
                raise SyntaxError('SyntaxError: invalid token type. Expected keyword if,while,let,do,return.')
        
        
    def compileLet(self):
        pass

    def compileIf(self):
        pass

    def compileWhile(self):
        pass

    def compileDo(self):
        pass

    def compileReturn(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass

