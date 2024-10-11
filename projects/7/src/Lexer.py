import re

class Lexer(object):
    def __init__(self, file_path):
        file = open(file_path, 'r')
        self.lines = file.read()
        


    def tokenize(self, lines):
        pass

