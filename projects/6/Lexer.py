import re


#loads asm file, does some cleanup and tokenizes it
def read_asm_file(file_path):
    lines = []  
    try:
        with open(file_path, 'r') as file:
            
            for line in file:
                stripped_line = line.strip()  
                if stripped_line:
                    tokens = stripped_line.split()
                    lines.append(tokens)
    except FileNotFoundError:
        print(f"file was not found: {file_path}")
    except Exception as e:
        print(f"error: {e}")
    
    return lines


def tokenize(line):
    tokens = re.findall(r'@?\w+|[=;]', line)

    return tokens

def lexer():
    asm_code = read_asm_file("projects/6/pong/Pong.asm")

    #strips comments from asm code
    stripped_asm_code = []
    for line in asm_code:
        line = ' '.join(line)
        if '//' in line:
            comment_index = line.index('//')
            if comment_index == 0: #if whole line is comment, just skip
                continue
            else: #strips the comment if its after instruction
                stripped_asm_code.append(line[:comment_index])
        else:
            stripped_asm_code.append(line)
    
    #tokenize
    tokens = []
    for line in stripped_asm_code:
        token = tokenize(line)
        tokens.append(token)

    return tokens
    

