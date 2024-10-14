from Helper import *


class CodeWriter(object):
    def __init__(self, outfile):
        self.outfile = open(outfile, "w")
        self.label_count = 0

    def write_arithmetic(self, command):
        if command == "add": self.write_arithmetic_add("D+A")
        elif command == "sub": self.write_aritmetic_sub("D-A")
        elif command == "neg": self.write_arithmetic_neg("-D")
        elif command == "eq": self.write_arithmetic_eq("JEQ")
        elif command == "gt": self.write_arithmetic_gt("JGT")
        elif command == "lt": self.write_arithmetic_lt("JLT")
        elif command == "and": self.write_arithmetic_and("D&A")
        elif command == "or": self.write_arithmetic_or("D|A")
        elif command == "not": self.write_arithmetic_or("!D")
    

    #First we decrement Stack Pointer to get value on the stack
    #We save this value to to register D
    #Then we decrement stack pointer again to get another value from the stack
    #We save that value to another register
    #Then we add those values
    #After that we save the value at the stack pointer index and increment stack pointer value for next operation
    def write_arithmetic_add(self, comp):
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.decrement_sp()
        self.push_stack_to_dest("A")
        self.c_command("D", comp)
        self.push_comp_to_stack("D")
        self.sp_increment()
    
    #same process as add
    def write_aritmetic_sub(self, comp):
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.decrement_sp()
        self.push_stack_to_dest("A")
        self.c_command("D", comp)
        self.push_comp_to_stack("D")
        self.sp_increment()
    
    #In this case we just need to get 1 value and perform operation on that
    def write_arithmetic_neg(self, comp):
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.c_command("D", comp)
        self.push_comp_to_stack("D")
        self.sp_increment()

    def write_arithmetic_eq(self, jump):
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.decrement_sp()
        self.push_stack_to_dest("A")
        self.c_command("D", "A-D")

        label_true = f"TRUE_{self.label_count}"
        label_end = f"END_{self.label_count}"
        self.label_count += 1

        #if d == 0 jump to true
        self.push_comp_to_stack("0")
        self.a_command(label_end)
        self.c_command(None, "0", "JMP")

        #true label -> push -1 to the stack
        self.write_label(label_true)
        self.push_comp_to_stack("-1")

        #end label to continue execution
        self.write_label(label_end)

        self.sp_increment()


    def write_arithmetic_gt(self, jump):
        pass

    def write_arithmetic_lt(self, jump):
        pass

    #same as add
    def write_arithmetic_and(self, comp):
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.decrement_sp()
        self.push_stack_to_dest("A")
        self.c_command("D", comp)
        self.push_comp_to_stack("D")
        self.sp_increment()

    def write_arithmetic_or(self, comp):
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.decrement_sp()
        self.push_stack_to_dest("A")
        self.c_command("D", comp)
        self.push_comp_to_stack("D")
        self.sp_increment()

    def write_arithmetic_not(self, comp):
        pass

    def write_push_pop(self):
        pass

    def write_label(self):
        pass

    def write_goto(self):
        pass

    def write_if_goto(self):
        pass

    def write_function(self):
        pass

    def write_call(self):
        pass

    def write_return(self):
        pass

    def push(self, segment, index):
        pass

    #increment SP
    def sp_increment(self):
        self.a_command("SP")
        self.c_command("M", "M+1")
    #decrement SP
    def decrement_sp(self):
        self.a_command("SP")
        self.c_command("M", "M-1")

    def get_sp(self):
        self.a_command("SP")
        self.c_command("A", "M")

    #loads value to register
    def push_stack_to_dest(self, dest):
        self.get_sp()
        self.c_command(dest, "M")
    #pushes computed value to register
    def push_comp_to_stack(self, comp):
        self.get_sp()
        self.c_command("M", comp)

    def write_label(self, label):
        self.outfile.write(f"({label})\n")

    #writes A command to file
    def a_command(self, reg):
        self.outfile.write(f'@{reg}\n')

    #writes C command to file 
    def c_command(self, dest, comp, jump=None):
        """
        args:
            dest -> destination register
            comp -> computation part
            jump -> jump condition, if none we simply dont use it
        """
        command = ""
        if dest is not None:
            if not isinstance(dest, str):
                raise ValueError("Destination must be string")
            command += f"{dest}="
        
        if not isinstance(comp, str):
            raise ValueError("Comp must be a string")
        command += comp

        if jump is not None:
            if not isinstance(jump, str):
                raise ValueError("Jump must be a string")
            command += f";{jump}"
        self.outfile.write(command + "\n0")
