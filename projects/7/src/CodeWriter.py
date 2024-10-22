from Helper import *


class CodeWriter(object):
    def __init__(self, outfile):
        self.outfile = open(outfile, "w")
        self.label_count = 0

    def close_file(self):
        self.outfile.close()

    def write_arithmetic(self, command):
        if command[0][1] == "add": self.write_arithmetic_add("D+A")
        elif command[0][1] == "sub": self.write_aritmetic_sub("D-A")
        elif command[0][1] == "neg": self.write_arithmetic_neg("-D")
        elif command[0][1] == "eq": self.write_arithmetic_eq("JEQ")
        elif command[0][1] == "gt": self.write_arithmetic_gt("JGT")
        elif command[0][1] == "lt": self.write_arithmetic_lt("JLT")
        elif command[0][1] == "and": self.write_arithmetic_and("D&A")
        elif command[0][1] == "or": self.write_arithmetic_or("D|A")
        elif command[0][1] == "not": self.write_arithmetic_or("!D")
    

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
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.decrement_sp()
        self.push_stack_to_dest("A")
        self.c_command("D", "A-D")
        label_true = f"TRUE_{self.label_count}"
        label_end = f"END_{self.label_count}"
        self.label_count += 1

        self.a_command(label_true)
        self.c_command(None, "D", "JGT")

        self.push_comp_to_stack("0")
        self.a_command(label_end)
        self.c_command(None, "0", "JMP")

        self.write_label(label_true)
        self.push_comp_to_stack("-1")
        
        self.write_label(label_end)

        self.sp_increment()

    def write_arithmetic_lt(self, jump):
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.decrement_sp()
        self.push_stack_to_dest("A")

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
        self.decrement_sp()
        self.push_stack_to_dest("D")
        self.c_command("D", comp)
        self.push_comp_to_stack("D")
        self.sp_increment()

    def write_push(self, segment, index):
        if segment == "constant":
            self.write_push_constant(index)
        elif segment in ['local', 'argument', 'this', 'that']:
            self.write_push_lcl_arg_this_that(segment, index)
        elif segment == "temp":
            self.write_push_temp(index)
        elif segment == "pointer":
            self.write_push_pointer(index)
        elif segment == "static":
            self.write_push_static(index)
    
    def write_push_lcl_arg_this_that(self, segment, index):
        seg_map = {
            "local":"LCL",
            "argument":"ARG",
            "this":"THIS",
            "that":"THAT"
        }

        base_addr = seg_map.get(segment)

        if base_addr is None:
            raise ValueError(f"Invalid segment syntax: {segment}")
        
        int_index = int(index)
        
        self.a_command(base_addr)
        self.c_command("D", "M")

        self.a_command(int_index)
        self.c_command("A", "D+A")

        self.c_command("D", "M")

        self.push_comp_to_stack("D")

        self.sp_increment()


    def write_push_temp(self, index):
        base_addr = 5 #starts at R5

        temp_addr = base_addr + int(index)

        self.a_command(temp_addr)
        self.c_command("D", "M")
        self.push_comp_to_stack("D")
        self.sp_increment()


    def write_pop(self, segment, index):
        if segment in ["local", "argument", "this", "that"]:
            self.write_pop_lcl_arg_this_that(segment, index)
        elif segment == "temp":
            self.write_pop_temp(index)
        elif segment == "pointer":
            self.write_pop_pointer(index)
        elif segment == "static":
            self.write_pop_static(index)

    def write_pop_lcl_arg_this_that(self, segment, index):
        seg_map = {
            "local":"LCL",
            "argument":"ARG",
            "this":"THIS",
            "that":"THAT"
        }

        base_addr = seg_map.get(segment)
        if base_addr is None:
            raise ValueError(f"Invalid seg syntax: {segment}")
        
        int_index = int(index)

        self.a_command(base_addr)
        self.c_command("D", "M")

        self.a_command(int_index)
        self.c_command("D", "D+A")

        self.a_command("R13")
        self.c_command("M", "D")

        self.decrement_sp()
        self.get_sp()
        self.c_command("D", "M")

        self.a_command("R13")
        self.c_command("A", "M")
        self.c_command("M", "D")

    def write_pop_temp(self, index):
        base_addr = 5
        temp_addr = base_addr + int(index)

        self.decrement_sp()
        self.get_sp()
        self.c_command("M", "D")


    def write_label(self, label):
        self.outfile.write(f"({label})\n")

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

    def write_push_constant(self, index):
        self.a_command(index)
        self.c_command("D", "A")
        self.push_d_to_stack()

    def push_d_to_stack(self):
        self.get_sp()
        self.c_command("M", "D")
        self.sp_increment()

    def pop_stack_to_d(self):
        self.decrement_sp()
        self.get_sp()
        self.c_command("D", "M")
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
        self.outfile.write(command + "\n")
