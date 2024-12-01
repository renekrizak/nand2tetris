
class VMWriter:
    def __init__(self, outfile):
        self.outfile = outfile

    def writeFile(self, line):
        with open(self.outfile, 'a') as out:
            out.write(f'{line}\n')

    """
    Add checks for all write commands
    """
    def writePush(self, segment: str, index: int):
        self.writeFile(f'push {segment} {index}')

    def writePop(self, segment: str, index: int):
        self.writeFile(f'pop {segment} {index}')

    def writeArithmetic(self, command: str):
        self.writeFile(f'{command}')

    def writeLabel(self, label: str):
        self.writeFile(f'label {label}')

    def writeGoto(self, label: str):
        self.writeFile(f'goto {label}')

    def writeIf(self, label: str):
        self.writeFile(f'if-goto {label}')

    def writeCall(self, name: str, nArgs: int):
        self.writeFile(f'call {name} {nArgs}')

    def writeFunction(self, name: str, nVars: int):
        self.writeFile(f'function {name} {nVars}')

    def writeReturn(self):
        self.writeFile('return')

