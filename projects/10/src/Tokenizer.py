import re
#Tokenizes the input

class Tokenizer():
    def __init__(self, input_file):
        pass

    def tokenize(self, fp):
        lines = []
        try:
            with open(fp, "r") as file:
                for line in file:
                    stripped_line = line.strip()
                    if stripped_line:
                        print(stripped_line)
                        tokens = stripped_line.split()
                        lines.append(tokens)
        
        except FileNotFoundError:
            print(f"File {file} was not found")
        except Exception as e:
            print(f"Error: {e} occured")

    def hasMoreTokens(self):
        pass
    
    def advance(self):
        pass

    def tokenType(self):
        pass

    def keyWord(self):
        pass

    def symbol(self):
        pass
    
    def identifier(self):
        pass

    def intVal(self):
        pass

    def stringVal(self):
        pass 