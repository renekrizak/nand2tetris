import re
#Tokenizes the input

class Tokenizer():
    def __init__(self, input_file):
        pass

    def tokenize(self, fp):
        try:
            with open(fp, "r") as file:
                pass
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