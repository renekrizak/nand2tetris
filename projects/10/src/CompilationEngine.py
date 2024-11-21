#Parses the tokenized jack code
"""
Rules:
class → 'class' className '{' classVarDec* subroutineDec* '}'
classVarDec → ('static' | 'field') type varName (',' varName)* ';'
subroutineDec → ('constructor' | 'function' | 'method') ('void' | type) subroutineName
                '(' parameterList ')' subroutineBody
parameterList → ((type varName) (',' type varName)*)?
subroutineBody → '{' varDec* statements '}'
varDec → 'var' type varName (',' varName)* ';'
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
    
    def consume(self):
        if not self.current_token:
            raise SyntaxError("unexpected end of tokens")
         

    def compileClass(self):
        pass

    def compileClassVarDec(self):
        pass

    def compileSubroutine(self):
        pass

    def compileStatements(self):
        pass
    
    def compileExpression(self):
        pass
