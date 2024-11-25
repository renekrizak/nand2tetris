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
        """
        letStatement → 'let' varName ('[' expression ']')? '=' expression ';'
        """
        self.consume('keyword', 'let')

        if self.current_token[0] != 'identifier':
            raise SyntaxError(f"Expected variable name, instead got: {self.current_token}")

        self.advance()

        if self.current_token == ('symbol', '['):
            self.advance()
            self.compileExpression()
            if self.current_token != ('symbol', ']'):
                raise SyntaxError(f'Expected closing parantheses, instead got: {self.current_token}')
            self.advance()

        self.consume('symbol', '=')

        self.compileExpression()

        self.consume('symbol', ';')


    def compileIf(self):
        """
        ifStatement → 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self.consume('keyword', 'if')
        self.consume('symbol', '(')
        self.compileExpression()
        self.consume('symbol', ')')

        self.consume('symbol', '{')
        self.compileStatements()
        self.consume('symbol', '}')

        if self.current_token == ('keyword', 'else'):
            self.consume('keyword', 'else')
            self.consume('symbol', '{')
            self.compileStatements()
            self.consume('symbol', '}')

    def compileWhile(self):
        """
        whileStatement → 'while' '(' expression ')' '{' statements '}'
        """
        self.consume('keyword', 'while')
        self.consume('symbol', '(')
        self.compileExpression()
        self.consume('symbol', ')')
        self.consume('symbol', '{')
        self.compileStatements()
        self.consume('symbol', '}')

    def compileDo(self):
        """
        doStatement → 'do' subroutineCall ';'
        """

        self.consume('keyword', 'do')
        self.compileSubroutineCall()
        self.consume('symbol', ';')

    def compileReturn(self):
        """
        returnStatement → 'return' expression? ';'
        """

        self.consume('keyword', 'return')
        if self.current_token != ('symbol', ';'):
            self.compileExpression()
        self.consume('symbol', ';')

    def compileExpression(self):
        """
        expression → term (op term)*
        """

        self.compileTerm()

        while self.current_token and self.current_token[0] == 'symbol' and self.current_token[1] in "+-*/&|<>=":
            self.advance()
            self.compileTerm()



    def compileTerm(self):
        """
        term → integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' 
            | subroutineCall | '(' expression ')' | unaryOp term
        """
        if self.current_token[0] == 'integer':
            self.advance()
            #make token to xml function
        elif self.current_token[0] == 'string':
            self.advance()
        elif self.current_token[0] == 'keyword':
            self.advance()
        elif self.current_token == ('symbol', '('):
            self.advance()
            self.compileExpression()
            if self.current_token != ('symbol', ')'):
                raise SyntaxError(f'Expected closing parantheses, instead got: {self.current_token}')
            self.advance()
        elif self.current_token[0] == 'symbol' and self.current_token[1] in '-~':
            self.advance()
            self.compileTerm()
        elif self.current_token[0] == 'identifier':
            next_token = self.tokens[self.index + 1] if self.index + 1 < len(self.tokens) else None
            if next_token == ('symbol', '['):
                self.advance()
                self.advance()
                self.compileExpression()
                if self.current_token != ('symbol', ']'):
                    raise SyntaxError(f'Expected closing brackets, instead got: {self.current_token}')
                self.advance()
            elif next_token in [('symbol', '('), ('symbol', '.')]:
                self.compileSubroutine()
            else:
                self.advance()
        else:
            raise SyntaxError(f"Invalid term: {self.current_token}")



    def compileExpressionList(self):
         """
        expressionList → (expression (',' expression)*)?
        """
         if self.current_token != ('symbol', ')'):
             self.compileExpression()

             while self.current_token == ('symbol', ','):
                 self.advance()
                 self.compileExpression()

    def compileSubroutineCall(self):
        """
        subroutineCall → subroutineName '(' expressionList ')' 
                   | (className | varName) '.' subroutineName '(' expressionList ')'
       """
        if self.current_token[0] != 'identifier':
            raise SyntaxError(f'Expected subroutineName, className or varName, instead got: {self.current_token}')
        self.advance()

        if self.current_token == ('symbol', '.'):
            self.advance()

            if self.current_token[0] != 'identifier':
                raise SyntaxError(f'Expected subroutine name after: .')
            self.advance()

            self.consume('symbol', '(')

            self.compileExpressionList()

            self.consume('symbol', ')')
