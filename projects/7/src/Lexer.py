import sys
from Helper import *
class Lexer(object):
    def __init__(self, file_path):
        file = open(file_path, 'r')
        self.lines = file.readlines()

    def remove_comments(self, stripped_line):
        comm_index = stripped_line.find('//')
        commentless_line = []
        if comm_index == -1:
            return stripped_line
        if comm_index == 0:
            pass
        else:
            commentless_line.append(stripped_line[:comm_index])

        return commentless_line
    def tokenize_line(self, line):
        tokens = []
        split_line = line.split()

        if len(split_line) == 0:
            return tokens
        
        command_type = split_line[0]
        tokens.append(('COMMAND_TYPE', command_type))

        if len(split_line) > 1:
            arg1 = split_line[1]
            tokens.append(('ARGUMENT', arg1))
        if len(split_line) > 2:
            arg2 = split_line[2]
            tokens.append(('NUMBER', arg2))
        return tokens
    #very simple check whether commands etc. are named correctly/exist
    def check_syntax(self, tokens):
        for line in tokens:
            for token in line:
                token_type, token_value = token
                #print(f"Token type: {token_type}, Token value: {token_value}")
                if token_type == "COMMAND_TYPE" and token_value not in commands:
                    sys.stderr.write(f'Command not found: type: {token_type} value: {token_value}')
                    break
                elif token_type == "ARGUMENT" and token_value not in args:
                    sys.stderr.write(f'Argument not found: type: {token_type} value: {token_value}')
                    break
                elif token_type == "NUMBER" and not token_value.isnumeric():
                    sys.stderr.write(f'Number is not correct format: type: {token_type} value: {token_value}')
                    break
        return None
    
    def tokenize(self):
        tokens = []
        for line in self.lines:
            stripped_line = line.strip()
            stripped_line = self.remove_comments(stripped_line)
            if stripped_line:
                line_tokens = self.tokenize_line(stripped_line)
                if line_tokens:
                    tokens.append(line_tokens)
        self.check_syntax(tokens)    
        return tokens

        