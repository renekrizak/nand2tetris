from Helper import *

class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_command = None
        self.current_index = -1
    
    def next_token_exists(self):
        return self.current_index < len(self.tokens) - 1

    def peek_next_token(self):
        self.current_index += 1
        self.current_command = self.tokens[self.current_index]

    def command_type(self):
        return self.current_command[0][1]    
    
    def get_arg1(self):
        if self.command_type() == "C_ARITHMETIC":
            return self.current_command[0][1]
        elif len(self.current_command) > 1:
            return self.current_command[1][1]
        return None

    def get_arg2(self):
        if len(self.current_command) > 2:
            return self.current_command[2][1]
        return None
    
    def parse_commands(self):
        parsed_commands = []

        while self.next_token_exists():
            self.peek_next_token()
            command_type = self.command_type()
            parsed_command = [("COMMAND_TYPE", command_type)]

            if self.get_arg1():
                parsed_command.append(("ARGUMENT", self.get_arg1()))
            if self.get_arg2():
                parsed_command.append(("NUMBER", self.get_arg2()))
            parsed_commands.append(parsed_command)
        
        return parsed_commands