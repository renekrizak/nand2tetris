

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
        self.subroutine_scope = {}
        self.index_counters['argument'] = 0
        self.index_counters['local'] = 0

    #adds to the table
    def define(self, name: str, type: str, kind: str):
        if kind in ('static', 'field'):
            self.class_scope[name] = {'type': type, 'kind': kind, 'index': self.index_counters[kind]}
        elif kind in ('argument', 'local'):
            self.subroutine_scope[name] = {'type': type, 'kind': kind, 'index': self.index_counters[kind]}
        else:
            raise SyntaxError(f'Invalid kind. Expected static, field, argument, local, instead got: {kind}')
    
        self.index_counters[kind] += 1

    #returns number of variables of given type in table
    def varCount(self, kind: str):
        if kind in ('static', 'field'):
            return sum(1 for symbol in self.class_scope.values() if symbol['kind'] == kind)
        elif kind in ('argument', 'local'):
            return sum(1 for symbol in self.subroutine_scope.values() if symbol['kind'] == kind)
        else:
            raise SyntaxError(f'Invalid kind. Expected static, field, argument, local, instead got: {kind}')

    #returns kind of identifier
    def kindOf(self, name: str):
        if name in self.class_scope:
            return self.class_scope[name]['kind']
        elif name in self.subroutine_scope:
            return self.subroutine_scope[name]['kind']
        return None
        

    #returns type of named var
    def typeOf(self, name: str):
        if name in self.class_scope:
            return self.class_scope[name]['type']
        elif name in self.subroutine_scope:
            return self.subroutine_scope[name]['type']
        return None

    #returns index of named var
    def indexOf(self, name: str):
        if name in self.class_scope:
            return self.class_scope[name]['index']
        elif name in self.subroutine_scope:
            return self.subroutine_scope[name]['index']
        return None