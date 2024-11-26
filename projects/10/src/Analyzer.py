#Main loop of the whole process
from Tester import XmlTreeTester
from Tokenizer import Tokenizer
from CompilationEngine import Parser
import sys, os

def get_filepath(filename):
    root_dir = os.path.abspath('..')
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == filename + ".jack":
                return os.path.join(root, file)
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python Analyzer.py <jack source file name>")
        print("No need to specify path, analyzer will look for the file name")
        return
    file_name = sys.argv[1]
    file_path = get_filepath(file_name) 
    if file_path == None:
        print(f"File ${file_name} was not found")
    
    tokenizer = Tokenizer(file_path)    
    tokens = tokenizer.tokenize()
    
    parser = Parser(tokens)
    parser.compileClass()
    parser.writeToXML(f'{file_name}_output.xml')

    file_path = file_path[:-5]
    compiled_xml_file = f"{file_name}_output.xml"
    original_xml_file = f"{file_path}.xml"
    tester = XmlTreeTester()
    tester.load_and_compare(compiled_xml_file, original_xml_file)




main()