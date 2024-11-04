#Main loop of the whole process
from Tester import XmlTreeTester

def main():

    original_xml_file = "Main.xml"
    compiler_xml_file = "Test.xml"
    tester = XmlTreeTester()
    tester.load_and_compare(original_xml_file, compiler_xml_file)

main()