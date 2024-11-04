import xml.etree.ElementTree as ET
import logging

class XmlTreeTester():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG) 
        self.hdlr = logging.FileHandler('xml-comp.log')
        self.logger.addHandler(self.hdlr)
    
    @staticmethod 
    def convert_string_to_tree(xmlString):
        return ET.fromstring(xmlString)
    
    def xml_compare(self, x1, x2):
        if x1.tag != x2.tag:
            self.logger.debug("Tags dont match: %s and %s" % (x1.tag, x2.tag))
            return False
        for name, value in x1.attrib.items():
            if x2.attrib.get(name) != value:
                self.logger.debug("Attributes dont match %s=%r, %s=%r" % (name, value, name, x2.attrib.get(name)))
                return False
        for name in x2.attrib.keys():
            if name not in x1.attrib:
                self.logger.debug("x2 has attribute that x1 doesnt: %s" % name)
                return False
        if not self.text_compare(x1.text, x2.text):
            self.logger.debug("text: %r != %r" % (x1.text, x2.text))
            return False
        if not self.text_compare(x1.tail, x2.tail):
            self.logger.debug("tail: %r != %r" % (x1.tail, x2.tail))
            return False
        children1 = list(x1)
        children2 = list(x2)
        if len(children1) != len(children2):
            self.logger.debug("children are different length: %i != %i" % (len(children1), len(children2)))
            return False
        i = 0
        for children1, children2 in zip(children1, children2):
            i += 1
            if not self.xml_compare(children1, children2):
                self.logger.debug("children %i dont match %s" % (i, children1.tag))
                return False
            
        return True
    
    def text_compare(self, t1, t2):
        if not t1 and not t2:
            return True
        if t1 == '*' or t2 == '*':
            return True
        return (t1 or '').strip() == (t2 or '').strip()
    
    def load_and_compare(self, f1, f2):
        try:
            tree1 = ET.parse(f1)
            tree2 = ET.parse(f2)
            root1 = tree1.getroot()
            root2 = tree2.getroot()

            if self.xml_compare(root1, root2):
                self.logger.info("Files %s and %s are equal" % (f1, f2))
                print("Files are the same")
            else:
                self.logger.info("Files %s and %s are not equal" % (f1, f2))
                print("Files are different")
        except ET.ParseError as e:
            self.logger.error("Failed to parse XML file %s" % e)
            print("Failed to parse XML files", e)