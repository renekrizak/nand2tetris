from VMWriter import VMWriter
from SymbolTable import SymbolTable
class CompilationEngine:
    def __init__(self, tokens, outfile):
        self.tokens = tokens
        self.current_token = tokens[0] if tokens else None
        self.index = 0
        self.vm_writer = VMWriter(outfile)
        self.symbol_table = SymbolTable()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def compileClass(self):
        self.advance()
        class_name = self.current_token[1]
        self.class_name = class_name
        self.advance()
        self.advance()

        while self.current_token and self.current_token[1] in ('static', 'field'):
            self.compileClassVarDec()

        while self.current_token and self.current_token[1] in ('constructor', 'function', 'method'):
            self.compileSubroutine()

        self.advance()

    def compileClassVarDec(self):
        kind = self.current_token[1]
        self.advance()

        type = self.current_token[1]
        self.advance()

        var_name = self.current_token[1]
        self.symbol_table.define(var_name, type, kind)

        while self.current_token and self.current_token == ('symbol', ','):
            self.advance()
            var_name = self.current_token[1]
            self.symbol_table.define(var_name, type, kind)
        
        self.advance()


    def compileSubroutine(self):
        sub_type = self.current_token[1] #constructor, function or method
        self.advance()

        return_type = self.current_token[1]
        self.advance()

        sub_name = self.current_token[1]
        name = f'{self.class_name}.{sub_name}'
        self.advance()

        self.symbol_table.reset()

        if sub_type == 'method':
            self.symbol_table.define('this', self.class_name, 'argument')

        self.advance()
        self.compileParameterList()
        self.advance()
        self.compileSubroutineBody(name, sub_type)

    def compileParameterList(self):
        if self.current_token[0] != 'symbol' or self.current_token[1] != ')':
            type = self.current_token[1]
            self.advance()
            var_name = self.current_token[1]
            self.symbol_table.define(var_name, type, 'argument')
            self.advance()
        
        while self.current_token and self.current_token == ('symbol', ','):
            self.advance()
            type = self.current_token[1]
            self.advance()
            var_name = self.current_token[1]
            self.symbol_table.define(var_name, type, 'argument')
            self.advance()

    def compileSubroutineBody(self, name, subroutine_type):
        self.advance()

        while self.current_token[0] == 'keyword' and self.current_token[1] == 'var':
            self.compileVarDec()

        num_local = self.symbol_table.varCount('local')
        self.vm_writer.writeFunction(name, num_local)

        if subroutine_type == 'constructor':
            f_count = self.symbol_table.varCount('field')
            self.vm_writer.writePush('constant', f_count)
            self.vm_writer.writeCall('Memory.alloc', 1)
            self.vm_writer.writePop('pointer', 0)
        
        elif subroutine_type == 'method':
            self.vm_writer.writePush('argument', 0)
            self.vm_writer.writePop('pointer', 0)

        self.compileStatements()
        self.advance()

    def compileVarDec(self):
        self.advance()

        type = self.current_token[1]
        self.advance()

        var_name = self.current_token[1]
        self.symbol_table.define(var_name, type, 'local')
        self.advance()

        while self.current_token[0] == 'symbol' and self.current_token[1] == ',':
            self.advance()
            var_name = self.current_token[1]
            self.symbol_table.define(var_name, type, 'local')
            self.advance()

        self.advance()


    def compileStatements(self):
        
        while self.current_token[0] == 'keyword' and self.current_token[1] in ('let', 'if', 'while', 'do', 'return'):
            if self.current_token[1] == 'let':
                self.compileLet()
            elif self.current_token[1] == 'if':
                self.compileIf()
            elif self.current_token[1] == 'while':
                self.compileWhile()
            elif self.current_token[1] == 'do':
                self.compileDo()
            elif self.current_token[1] == 'return':
                self.compileReturn()
            else:
                break

    def compileLet(self):
        self.advance()
        var_name = self.current_token[1]
        self.advance()

        kind = self.symbol_table.kindOf(var_name)
        index = self.symbol_table.indexOf(var_name)
        segment = self.mapKindToSegment(kind)
        is_arr = False
        if self.current_token == ('symbol', '['):
            is_arr = True
            self.advance()
            self.compileExpression()
            self.vm_writer.writePush(segment, index)
            self.vm_writer.writeArithmetic('add')
            self.advance()
        
        self.advance()
        self.compileExpression()

        if is_arr:
            self.vm_writer.writePop('temp', 0)
            self.vm_writer.writePop('pointer', 0)
            self.vm_writer.writePush('temp', 0)
            self.vm_writer.writePop('that', 0)

        else:
            self.vm_writer.writePop(segment, index)

        self.advance()


    def compileIf(self):
        lbl_false = f'IF_FALSE_{self.genLabelInde()}'
        lbl_end = f'IF_END_{self.genLabelIndex()}'

        self.advance()
        self.advance()
        self.compileExpression()
        self.advance()

        self.vm_writer.writeArithmetic('not')
        self.vm_writer.writeIf(lbl_false)

        self.advance()
        self.compileStatements()
        self.advance()

        if self.current_token == ('keyword', 'else'):
            self.vm_writer.writeGoto(lbl_end)
            self.vm_writer.writeLabel(lbl_false)
            self.advance()
            self.advance()
            self.compileStatements()
            self.advance()
            self.vm_writer.writeLabel(lbl_end)
        else:
            self.vm_writer.writeLabel(lbl_false)

    def compileWhile(self):
        
        label_start = f"WHILE_START_{self.genLabelIndex()}"
        label_end = f"WHILE_END_{self.genLabelIndex()}"

        self.vm_writer.writeLabel(label_start)

        self.advance()
        self.advance()
        self.compileExpression()
        self.vm_writer.writeArithmetic('not')
        self.vm_writer.writeIf(label_end)
        self.advance()
        self.advance()
        self.compileStatements()
        self.vm_writer.writeGoto(label_start)
        self.vm_writer.writeLabel(label_end)
        self.advance()

    def compileDo(self):
        self.advance()
        self.compileSubroutineCall()
        self.vm_writer.writePop('temp', 0)
        self.advance()

    def compileReturn(self):
        self.advance()

        if self.current_token != ('symbol', ';'):
            self.compileExpression()
        else:
            self.vm_writer.writePush('constant', 0)

        self.vm_writer.writeReturn()
        self.advance()

    def compileExpression(self):
        self.compileTerm()

        op = None
        while self.current_token[0] == 'symbol' and self.current_token[1] in "+-*/&<>=":
            
            op = self.current_token[1]
            print(op)
            self.advance()
            self.compileTerm()
            operator_map = {
            '+': 'add',
            '-': 'sub',
            '*': 'call Math.multiply 2',
            '/': 'call Math.divide 2',
            '&': 'and',
            '|': 'or',
            '<': 'lt',
            '>': 'gt',
            '=': 'eq',
            }
       
            self.vm_writer.writeArithmetic(operator_map[op])
    def compileTerm(self):
    
        if self.current_token[0] == 'integer':  
            self.vm_writer.writePush('constant', int(self.current_token[1]))
            self.advance()
        elif self.current_token[0] == 'string': 
            self.vm_writer.writePush('constant', len(self.current_token[1]))
            self.vm_writer.writeCall('String.new', 1)
            for char in self.current_token[1]:
                self.vm_writer.writePush('constant', ord(char))
                self.vm_writer.writeCall('String.appendChar', 2)
            self.advance()
        elif self.current_token[0] == 'keyword':  
            self.compileKeyword(self.current_token[1])
            self.advance()
        elif self.current_token[0] == 'identifier':  
            var_name = self.current_token[1]
            self.advance()

            if self.current_token == ('symbol', '['):  
                self.advance()
                self.compileExpression()
                self.advance()
                kind = self.symbol_table.kindOf(var_name)
                index = self.symbol_table.indexOf(var_name)
                segment = self.mapKindToSegment(kind)
                self.vm_writer.writePush(segment, index)
                self.vm_writer.writeArithmetic('add')
                self.vm_writer.writePop('pointer', 1)
                self.vm_writer.writePush('that', 0)
            elif self.current_token in [('symbol', '('), ('symbol', '.')]:  
                self.compileSubroutineCall()  
            else:  
                kind = self.symbol_table.kindOf(var_name)
                index = self.symbol_table.indexOf(var_name)
                segment = self.mapKindToSegment(kind)
                self.vm_writer.writePush(segment, index)
        elif self.current_token[1] == '(': 
            self.advance()
            self.compileExpression()
            self.advance()
        elif self.current_token[1] in ['-', '~']:  
            unary_op = self.current_token[1]
            self.advance()
            self.compileTerm()
            self.vm_writer.writeArithmetic('neg' if unary_op == '-' else 'not')

    def compileExpressionList(self):
        n_args = 0

        if self.current_token != ('symbol', ')'):
            self.compileExpression()
            n_args += 1

            while self.current_token == ('symbol', ','):
                self.advance()
                self.compileExpression()
                n_args += 1
        return n_args

    def compileSubroutineCall(self):
        
        n_args = 0
        obj_name = None
        temp = self.tokens[self.index - 1]
        sub_name = temp[1] 

        if self.current_token == ('symbol', '.'):
            obj_name = sub_name
            self.advance()
            sub_name = self.current_token[1]
            self.advance()

        if obj_name:
            if self.symbol_table.kindOf(obj_name):
                kind = self.symbol_table.kindOf(obj_name)
                index = self.symbol_table.indexOf(obj_name)
                segment = self.mapKindToSegment(kind)
                self.vm_writer.writePush(segment, index)
                n_args += 1
                f_name = f'{self.symbol_table.typeOf(obj_name)}.{sub_name}'
            else:
                f_name = f'{obj_name}.{sub_name}'
        else:
            self.vm_writer.writePush('pointer', 0)
            n_args += 1
            f_name = f'{self.class_name}.{sub_name}'

        self.advance()
        n_args += self.compileExpressionList()
        self.advance()
        print(f_name)
        self.vm_writer.writeCall(f_name, n_args)


    def genLabelIndex(self):
        if not hasattr(self, '_label_index'):
            self._label_index = 0
        self._label_index += 1
        return self._label_index

    def compileKeyword(self, val):
        if val == 'true':
            self.vm_writer.writePush('constant', 0)
            self.vm_writer.writeArithmetic('not')

        elif val in ['false', 'null']:
            self.vm_writer.writePush('constant', 0)
        elif val == 'this':
            self.vm_writer.writePush('pointer', 0)

    def mapKindToSegment(self, kind):
        seg_map = {
            'static':'static',
            'field':'this',
            'argument':'argument',
            'local':'local'
        }
        return seg_map[kind]