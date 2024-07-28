import sys, os

current_func, current_file = "", ""
call_count = 0
CMPR_COUNTER = {"eq": 0, "gt": 0, "lt": 0}
SEGMENT_MAP = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
push_D ="@SP\nAM=M+1\nA=A-1\nM=D"

def parse_line(line):
	line = line.strip()
	line_part = line.partition("//")
	if line_part[0]: return [token for token in line_part[0].split()]
	else: return [""]
		
def c_stack(tokens):
    if tokens[1] =="local" or tokens[1] =="argument" or tokens[1] =="this" or tokens[1] =="that":
        if tokens[0] == "push": asm_code = f"@{tokens[2]}\nD=A\n@{SEGMENT_MAP[tokens[1]]}\nA=D+M\nD=M\n{push_D}"
        elif tokens[0] == "pop": asm_code = f"@{tokens[2]}\nD=A\n@{SEGMENT_MAP[tokens[1]]}\nD=D+M\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D"
    elif tokens[1] =="constant":
        if tokens[0] == "push": asm_code = f"@{tokens[2]}\nD=A\n{push_D}"
    elif tokens[1] =="static":
        if tokens[0] == "push": asm_code = f"@{current_file}.{tokens[2]}\nD=M\n{push_D}"
        elif tokens[0] == "pop": asm_code = f"@SP\nAM=M-1\nD=M\n@{current_file}.{tokens[2]}\nM=D"
    elif tokens[1] =="temp":
        if tokens[0] == "push": asm_code = f"@{5+int(tokens[2])}\nD=M\n{push_D}"
        elif tokens[0] == "pop": asm_code = f"@SP\nAM=M-1\nD=M\n@{5+int(tokens[2])}\nM=D"
    elif tokens[1] =="pointer":
        if int(tokens[2]) == 0: varname = "THIS"
        elif int(tokens[2]) == 1: varname = "THAT"
        else: raise Exception(f"Pointer segment index can be 0 or 1, not {tokens[2]}.")
        if tokens[0] == "push": asm_code = f"@{varname}\nD=M\n{push_D}"
        elif tokens[0] == "pop": asm_code = f"@SP\nAM=M-1\nD=M\n@{varname}\nM=D"
    else: raise Exception(f"Incorrect segment name '{tokens[1]}'.")
    return asm_code

def c_arithmetic(tokens):
    if tokens[0] == "add": asm_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D+M"
    elif tokens[0] == "sub": asm_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M-D"
    elif tokens[0] == "neg": asm_code = "@SP\nA=M-1\nM=-M"
    return asm_code

def c_logical(tokens):
    if tokens[0] == "and": asm_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D&M"
    elif tokens[0] == "or": asm_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D|M"
    elif tokens[0] == "not": asm_code = "@SP\nA=M-1\nM=!M"
    return asm_code

def c_comparison(tokens):
    global CMPR_COUNTER
    CMPR_COUNTER[tokens[0]] += 1
    label = f"end{tokens[0]}{CMPR_COUNTER[tokens[0]]}"
    asm_code = f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@{label}\nD;J{tokens[0].upper()}\n@SP\nA=M-1\nM=0\n({label})"
    return asm_code

def c_branching(tokens):
    label = f"{current_func}${tokens[1]}"
    if tokens[0] == "label": asm_code = f"({label})"
    elif tokens[0] == "goto": asm_code = f"@{label}\n0;JMP"
    elif tokens[0] == "if-goto": asm_code = f"@SP\nAM=M-1\nD=M\n@{label}\nD;JNE"
    return asm_code

def c_function(tokens):
    global call_count, current_func
    if tokens[0] == "function":
        current_func = tokens[1]
        nvars = int(tokens[2])
        asm_code = f"({current_func})"
        for i in range(nvars): asm_code += '\n' + c_stack(["push", "constant", "0"])
    elif tokens[0] == "call":
        current_func = tokens[1]
        nargs = int(tokens[2])
        call_count += 1
        ret_label = f"{current_func}$ret.{call_count}"
        asm_code = f"@{ret_label}\nD=A\n{push_D}\n@LCL\nD=M\n{push_D}\n@ARG\nD=M\n{push_D}\n@THIS\nD=M\n{push_D}\n@THAT\nD=M\n{push_D}\n@SP\nD=M\n@LCL\nM=D\n@{5+nargs}\nD=D-A\n@ARG\nM=D\n@{current_func}\n0;JMP\n({ret_label})"
    elif tokens[0] == "return":
        asm_code = f"@LCL\nD=M\n@5\nD=D-A\nA=D\nD=M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\nD=A+1\n@SP\nM=D\n@LCL\nD=M\n@R14\nAM=D-1\nD=M\n@THAT\nM=D\n@R14\nAM=M-1\nD=M\n@THIS\nM=D\n@R14\nAM=M-1\nD=M\n@ARG\nM=D\n@R14\nAM=M-1\nD=M\n@LCL\nM=D\n@R13\nA=M\n0;JMP"
    return asm_code
        
def translate_file(in_filename):
    global current_file
    current_file = os.path.basename(in_filename)[:-3]
    f = open(in_filename, 'r')
    asm = ""
    for line in f:
        tokens = parse_line(line)
        match tokens[0]:
            case "push" | "pop": asm += c_stack(tokens) + '\n'
            case "add" | "sub" | "neg": asm += c_arithmetic(tokens) + '\n'
            case "eq" | "gt" | "lt": asm += c_comparison(tokens) + '\n'
            case "and" | "or" | "not": asm += c_logical(tokens) + '\n'
            case "label" | "goto" | "if-goto": asm += c_branching(tokens) + '\n'
            case "function" | "call" | "return": asm += c_function(tokens) + '\n'
            case "": pass
            case _: raise Exception(f"Command not implemented: {tokens[0]}")
    f.close()
    return asm

def main(path):
    path = os.path.normpath(path)
    if os.path.isdir(path):
        asm = f"@256\nD=A\n@SP\nM=D\n{c_function(['call', 'Sys.init', '0'])}\n"
        for (root, dirs, files) in os.walk(path):
            for fn in files:
                if fn.endswith(".vm"): asm += translate_file(os.path.join(root, fn)) + "\n"
        out_filename = os.path.join(path, os.path.basename(path) + ".asm")
    elif os.path.isfile(path) and path.endswith(".vm"):
        asm = translate_file(path)
        out_filename = path[:-3] + ".asm"
    else:
        raise Exception("Invalid path. Must be a directory or a .vm file!")
    
    f_out = open(out_filename, 'w')
    f_out.write(asm)
    f_out.close()
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception(f"Usage: python3 {sys.argv[0]} <path>")
        sys.exit(1)
    main(sys.argv[1])
