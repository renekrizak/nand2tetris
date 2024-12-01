

class SymbolTable:
    def __init__(self):
        self.class_scope = {}
        self.subroutine_scope = {}
        self.index_counters = {
            'static': 0,
            'field': 0,
            'argument': 0,
            'local': 0
        }

    #empty sym table and reset indexes to 0. called when you compile subroutine declaration
    def reset(self):
        pass

    #adds to the table
    def define(self, name: str, type: str, kind: str):
        pass

    #returns number of variables of given type in table
    def varCount(self, kind: str):
        pass

    #returns kind of identifier
    def kindOf(self, name: str):
        pass

    #returns type of named var
    def typeOf(self, name: str):
        pass

    #returns index of named var
    def indexOf(self, name: str):
        pass