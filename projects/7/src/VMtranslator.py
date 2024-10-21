from Lexer import Lexer
from Parser import Parser
from CodeWriter import CodeWriter
import sys, os

class Translator(object):
    def __init__(self):
        pass

    def get_file_path(file_name):
        root_dir = os.path.abspath('..')
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file == file_name + ".vm":
                    return os.path.join(root, file)
        
        return None

def main():
    if len(sys.argv) < 2:
        print("Program usage: python VMtranslator.py <inputfile>")
        print("Go to src directory and use the command above from there")
        print("adding .vm to the file is not needed")
        return
    file_name = sys.argv[1]
    file_path = Translator.get_file_path(file_name)
    if(file_path):
        print(f"file found: {file_path}")
    else:
        print(f"File {file_name}.vm not found")
    
    lexer = Lexer(file_path)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    parsed_tokens = parser.parse_commands()
    write = CodeWriter(f"{file_name}.asm")
    print(parsed_tokens)

    for command in parsed_tokens:
        if command[0][1] == "push":
            write.write_push(command[1][1], command[2][1])
        elif command[0][1] == "pop":
            write.write_pop(command[1][1], command[2][1])
        else:
            write.write_arithmetic(command)
    write.close_file()
main()