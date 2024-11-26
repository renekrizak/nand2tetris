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
        self.output = []

    def writeToXML(self, filename):
        
        with open(filename, 'w') as xml_file:
            def indent(level):
                return " " * level
            
            level = 0
            for line in self.output:
                if line.startswith('<') and not line.startswith('</'):
                    xml_file.write(f"{indent(level)}{line}\n")
                    if not line.startswith('<symbol>') and not line.startswith('<identifier>'):
                        level += 1
                
                elif line.startswith('</'):
                    level -= 1
                    xml_file.write(f'{indent(level)}{line}\n')

                else:
                    xml_file.write(f'{indent(level)}{line}\n')
        

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
            raise SyntaxError(f"Expected token type: {expected_token_type}, got {token_type}, iteration: {self.index}")
        if expected_token_value and token_value != expected_token_value:
            raise SyntaxError(f"Expected token value {expected_token_value}, got {token_value}, iteration: {self.index}")
        
        if token_type == 'keyword':
            self.output.append(f'<keyword> {token_value} </keyword>')
        elif token_type == 'symbol':
            self.output.append(f'<symbol> {token_value} </symbol>')
        elif token_type == 'identifier':
            self.output.append(f'<identifier> {token_value} </identifier>')
        elif token_type == 'string':
            self.output.append(f'<stringConstant> {token_value} </stringConstant>')
        elif token_type == 'integer':
            self.output.append(f'<integerConstant> {token_value} </integerConstant>')

        self.advance()

    def compileClass(self):
        """
class → 'class' className '{' classVarDec* subroutineDec* '}
        """
        self.output.append('<class>')
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
        self.output.append('</class>')

    def compileClassVarDec(self):
        """
classVarDec → ('static' | 'field') type varName (',' varName)* ';'
        """
        self.output.append('<classVarDec>')
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
        self.output.append('</classVarDec>')

    def compileSubroutine(self):
        """
        subroutineDec → ('constructor' | 'function' | 'method') ('void' | type) subroutineName
                '(' parameterList ')' subroutineBody
        """
        self.output.append('<subroutineDec>')
        
        if self.current_token not in [('keyword', 'constructor'), ('keyword', 'function'), ('keyword', 'method')]:
            raise SyntaxError(f'Expected constructor | function | method, instead got: {self.current_token[1]}')
        self.consume('keyword', self.current_token[1])

        if self.current_token[0] == 'keyword' and self.current_token[1] in ('void', 'int', 'char', 'boolean'):
            self.consume('keyword')
        elif self.current_token[0] == 'identifier':
            self.consume('identifier')
        else:
            raise SyntaxError(f'Expected void, primitive type or class name, instead got: {self.current_token}')
        
        if self.current_token[0] != 'identifier':
            raise SyntaxError(f'Expected subroutine name, instead got: {self.current_token}')
        self.consume('identifier', self.current_token[1])

        self.consume('symbol', '(')
        self.compileParameterList()
        self.consume('symbol', ')')

        self.compileSubroutineBody()

        self.output.append('</subroutineDec>')

    def compileParameterList(self):
        self.output.append('<parameterList>')
        if self.current_token and self.current_token[0] in ('keyword', 'identifier'):
            self.consume('keyword' if self.current_token[0] == 'keyword' else 'identifier')
            self.consume('identifier')

            while self.current_token and self.current_token == ('symbol', ','):
                self.consume('symbol', ',')
                self.consume('keyword' if self.current_token[0] == 'keyword' else 'identifier')
                self.consume('identifier')
        self.output.append('</parameterList>')

    def compileSubroutineBody(self):
        """
            subroutineBody → '{' varDec* statements '}'
        """

        self.output.append('<subroutineBody>')
        self.consume("symbol", "{")

        while self.current_token and self.current_token == ("keyword", 'var'):
            self.compileVarDec()

        self.compileStatements()

        self.consume('symbol', '}')

        self.output.append('</subroutineBody>')
    def compileVarDec(self):
        """
        varDec → 'var' type varName (',' varName)* ';'
        """
        self.output.append('<varDec>')
        self.consume('keyword', 'var')

        if self.current_token[0] == 'keyword' and self.current_token[1] in ('int', 'char', 'boolean'): self.consume('keyword')
        elif self.current_token[0] == 'identifier':
            self.consume('identifier')
        else:
            raise SyntaxError("Expected types: int, char, boolean")
        
        self.consume('identifier')

        while self.current_token and self.current_token == ('symbol', ','):
            self.consume('symbol', ',')
            self.consume('identifier')

        self.consume('symbol', ';')

        self.output.append('</varDec>')
    def compileStatements(self):
        """
        statements → statement*
        statement → letStatement | ifStatement | whileStatement | doStatement | returnStatement
        """
        self.output.append('<statements>')
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
        
        
        self.output.append('</statements>')
    def compileLet(self):
        """
        letStatement → 'let' varName ('[' expression ']')? '=' expression ';'
        """
        self.output.append('<letStatement>')
        self.consume('keyword', 'let')

        if self.current_token[0] != 'identifier':
            raise SyntaxError(f"Expected variable name, instead got: {self.current_token}")

        self.consume('identifier')

        if self.current_token == ('symbol', '['):
            self.consume('symmbol', '[')
            self.compileExpression()
            if self.current_token != ('symbol', ']'):
                raise SyntaxError(f'Expected closing parantheses, instead got: {self.current_token}')
            self.consume('symbol', ']')

        self.consume('symbol', '=')

        self.compileExpression()

        self.consume('symbol', ';')

        self.output.append('</letStatement>')

    def compileIf(self):
        """
        ifStatement → 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self.output.append('<ifStatement>')
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

        self.output.append('</ifStatement>')
    def compileWhile(self):
        """
        whileStatement → 'while' '(' expression ')' '{' statements '}'
        """
        self.output.append('<whileStatement>')
        self.consume('keyword', 'while')
        self.consume('symbol', '(')
        self.compileExpression()
        self.consume('symbol', ')')
        self.consume('symbol', '{')
        self.compileStatements()
        self.consume('symbol', '}')

        self.output.append('</whileStatement>')
    def compileDo(self):
        """
        doStatement → 'do' subroutineCall ';'
        """
        self.output.append('<doStatement>')
        self.consume('keyword', 'do')

        if self.current_token[0] != 'identifier':
            raise SyntaxError(f'Expected subroutine, className or varName, instead got: {self.current_token}')
        self.consume('identifier')

        if self.current_token == ('symbol', '.'):
            self.consume('symbol', '.')
            if self.current_token[0] != 'identifier':
                raise SyntaxError(f'expected subroutine name after . , instead got: {self.current_token}')
            self.consume('identifier')

        self.consume('symbol', '(')
        self.compileExpressionList()
        self.consume('symbol', ')')

        self.consume('symbol', ';')     
        self.output.append('</doStatement>')

    def compileReturn(self):
        """
        returnStatement → 'return' expression? ';'
        """
        self.output.append('<returnStatement>')
        self.consume('keyword', 'return')
        if self.current_token != ('symbol', ';'):
            self.compileExpression()
        self.consume('symbol', ';')
        self.output.append('</returnStatement>')

    def compileExpression(self):
        """
        expression → term (op term)*
        """
        self.output.append('<expression>')
        self.compileTerm()

        while self.current_token and self.current_token[0] == 'symbol' and self.current_token[1] in "+-*/&|<>=":
            self.output.append(f'<symbol> {self.current_token[1]} </symbol')
            self.advance()
            self.compileTerm()


        self.output.append('</expression>')

    def compileTerm(self):
        """
        term → integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' 
            | subroutineCall | '(' expression ')' | unaryOp term
        """
        self.output.append('<term>')

        if self.current_token[0] == 'integer':
            self.consume('integer')

        elif self.current_token[0] == 'string':
            self.consume('string')
        
        elif self.current_token[0] == 'keyword' and self.current_token[1] in {'true', 'false', 'null', 'this'}:
            self.consume('keyword')

        elif self.current_token == ('symbol', '('):
            self.consume('symbol', '(')
            self.compileExpression()
            self.consume('symbol', ')')

        elif self.current_token[0] == 'symbol' and self.current_token[1] in '-~':
            self.consume('symbol')
            self.compileTerm()
        
        elif self.current_token[0] == 'identifier':
            next_token = self.tokens[self.index + 1] if self.index + 1 < len(self.tokens) else None

            if next_token == ('symbol', '['):
                self.consume('identifier')
                self.consume('symbol', '[')
                self.compileExpression()
                self.consume('symbol', ']')
            
            elif next_token in [('symbol', '('), ('symbol', '.')]:
                self.compileSubroutine()

            else:
                self.consume('identifier')

        self.output.append('</term>')


    def compileExpressionList(self):
         """
        expressionList → (expression (',' expression)*)?
        """
         self.output.append('<expressionList>')
         if self.current_token != ('symbol', ')'):
             self.compileExpression()

             while self.current_token == ('symbol', ','):
                 self.consume('symbol', ',')
                 self.compileExpression()

         self.output.append('</expressionList>')

    def compileSubroutineCall(self):
        """
        subroutineCall → subroutineName '(' expressionList ')' 
                   | (className | varName) '.' subroutineName '(' expressionList ')'
       """
        self.output.append('<subroutineCall>')
        if self.current_token[0] != 'identifier':
            raise SyntaxError(f'Expected subroutineName, className or varName, instead got: {self.current_token}')
        self.consume('identifier')

        if self.current_token == ('symbol', '.'):
            self.consume('symbol', '.')

            if self.current_token[0] != 'identifier':
                raise SyntaxError(f'Expected subroutine name after: .')
            self.consume('identifier')

        self.consume('symbol', '(')

        self.compileExpressionList()

        self.consume('symbol', ')')

        self.output.append('</subroutineCall>')