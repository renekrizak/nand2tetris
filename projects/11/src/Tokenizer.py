import re
#Tokenizes the input

class Tokenizer():
    def __init__(self, input_file):
        file = open(input_file, "r")
        self.line = file.readlines()
        self.keywords = ["class", "constructor", "function", "method", "field", "static", "var",
            "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
            "do", "if", "else", "while", "return"]
        self.token_patterns = {
            "keyword": r'\b(?:' + '|'.join(self.keywords) + r')\b',  
            "identifier": r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',  
            "integer": r'\b\d+\b',  
            "string": r'"([^"]*)"',  
            "symbol": r'[{}()[\].,;+\-*/&|<>=~]',  
            "comment": r'//[^\n]*|/\*[\s\S]*?\*/',  
            "whitespace": r'\s+' 
        }


    def tokenize_line(self, line):
        """
        tokenizes single line and returns list of tokens
        """
        tokens = []
        while line:
            match = None
            for token_type, pattern in self.token_patterns.items():
                match = re.match(pattern, line)
                if match:
                    token = match.group(0)
                    if token_type != "whitespace":
                        tokens.append((token_type, token))
                    line = line[len(token):]  # consumes matched token
                    break
            if not match:
                raise ValueError(f"Unrecognized token in the input: {line[:20]}...")
        return tokens

    def tokenize(self):
        tokens = []
        comment_flag = False
        for line in self.line:
            #removes comments  & removes \n 
            line, comment_flag = self.remove_comments(comment_flag, line)
            line = line.replace("\n", "").strip()

            tokens.extend(self.tokenize_line(line))
        return tokens


    def remove_comments(self, flag, line):
        comment_index = line.find('//') #detects single line comments
        multiline_comm = line.find("/**") #detects multi line comments

        # checks if we found multi line comment entry. .find() returns -1 if element is not found at any index
        if multiline_comm != -1:
            flag = True

        # basically just checks if we are at the end of multiline comment
        # once we find */, we know the multiline comment is gonna end so we set flag to false 
        if flag:
            multiline_end = line.find('*/') # if we find end of multiline comment we return nothing and change flag to false
            if multiline_end >= 0:
                return "", False
            return "", True
        
        #if no multi lines we just check for single lines
        if comment_index == -1:
            return line, False
        if comment_index == 0:
            return "", False
        return line[:comment_index].strip(), False
    
