import Lexer
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
    

main()