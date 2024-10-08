import re
from Lexer import lexer
from Helper import *


#returns padded binary value
def dec2bin(n):
    return format(n, '016b')
#if symbol with mem address alredy exists, simply returns
#if not present, checks if next address is not alredy occupied
#if it is, loops until next address is free, then adds it to symbolTable if it appears in the code later
def get_symb_val(symbol, nextAddress, usedAddress):
    if symbol in symbolTable:
        bin_symb = dec2bin(symbolTable[symbol])
        return bin_symb
    if dec2bin(nextAddress) in usedAddress.values():
        while dec2bin(nextAddress) in usedAddress.values():
            nextAddress += 1
        symbolTable[symbol] = nextAddress
    bin_symbol = symbolTable[symbol]
    
    return dec2bin(bin_symbol)
        
#goes over all instructions and adds e.g. @21 to used addr
#to prevent conflict when addressing lets say @i, which could end up at the same address
def a_instruct_used_mem(tokens):
    usedAddr = {}
    for line in tokens:
        symbol = line[0][1:]
        if symbol.isnumeric():
            mem = dec2bin(int(symbol))
            usedAddr[symbol] = mem
    return usedAddr

#strips @ from the instruction, if its number simply returns binary form of given symbol
def process_a_instruction(line, nextAddress, usedAddresses):
    line = line[0][1:]
    if line.isnumeric(): #returns value of whole num A instruction
        return dec2bin(int(line))
    else: #returns address of symbol eg. @i
        return get_symb_val(line, nextAddress, usedAddresses)
    
def get_a_bit_val(line, length):
    if length < 3:
        return "0"
    temp = ''.join(line[2:])
    if temp in compCodesA:
        return "0"
    else:
        return "1"
#basically just compares with dictionary keys and returns the value
#pretty bad solution, but seems to work
def get_c_bits_vals(line, length):
    if length == 2:
        return "101010"
    temp = ''.join(line[2:])
    if temp in compCodesA:
        c_code = compCodesA[temp]
        return c_code
    else:
        return compCodesM[temp]
    
def get_jmp_dest_bits(line):
    dest_bits = "000"
    jump_bits = "000"
    
    if '=' in line:
        dest_index = line.index('=') 
        if dest_index > 0 and line[dest_index - 1] in destCodes:
            dest_bits = destCodes[line[dest_index - 1]]  
    
    if line[-1] in jumpCodes:
        jump_bits = jumpCodes[line[-1]]  
    
    return dest_bits + jump_bits

#First 3 bits always 1,
#4th a bit determined by what register is used -> 0 when a register, 1 when m register is used
#determining comp bits easy, we just gotta do dict lookup
#c instruction format -> dest=comp;jump
#dest or jump fields may be empty, if dest is empty = is omitted, if jump is empty ; is omitted 
def process_c_instruction(line):
    c_instruction = "111"
    length = get_line_length(line)
    c_instruction += get_a_bit_val(line, length)
    c_instruction += get_c_bits_vals(line, length)
    c_instruction += get_jmp_dest_bits(line)
    return c_instruction


def get_line_length(line):
    return len(line)


def Assemble():
    tokens = lexer()
    final = []
    usedAddresses = a_instruct_used_mem(tokens)
    nextAddress = 16
    print(usedAddresses)
    file2 = open("temp.hack", "w")
    for line in tokens:
        if line[0].startswith('@'):
            ainst = process_a_instruction(line, nextAddress, usedAddresses)
            file2.write(ainst + "\n")
            final.append(ainst)
        else:
            cinst = process_c_instruction(line)
            file2.write(cinst + "\n")
            final.append(cinst)
            

Assemble()



