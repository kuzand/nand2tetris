import sys
import os

# Global variables
current_func = ""
current_file = ""
call_count = 0
eq_counter = 0
gt_counter = 0
lt_counter = 0

push_D ="@SP\n"    \
        "AM=M+1\n" \
        "A=A-1\n"  \
        "M=D"


def basename(path):
    bn = []
    for i in range(len(path) - 1, -1, -1):
        c = path[i]
        if c == '/':
            break
        bn.append(c)

    n = len(bn)
    for i in range(n // 2):
        tmp = bn[i]
        bn[i] = bn[n - 1 - i]
        bn[n - 1 - i] = tmp

    return "".join(bn)


def parse_line(line):
    is_token = False
    token_count = 0
    tokens = ["", "", ""]
    token = ""
    for c in line:
        if c == '/':
            break
        elif c == '\n':
            if is_token:
                tokens[token_count - 1] = token
            break
        elif c == ' ' or c == '\t':
            if is_token:
                tokens[token_count - 1] = token
                is_token = False
        else:
            if not is_token:
                token = ""
                token_count +=1
                is_token = True
            token += c
    return tokens


def segment_map(segment):
    varname = ""
    if segment == "local":
        varname = "LCL"
    elif segment == "argument":
        varname = "ARG"
    elif segment == "this":
        varname = "THIS"
    else:
        varname = "THAT"
    return varname


def c_stack(cmd, segment, i):
    if cmd == "push":
        if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            varname = segment_map(segment)
            asm_code = \
                    f"@{i}\n" \
                    "D=A\n" \
                    f"@{varname}\n" \
                    "A=D+M\n" \
                    "D=M\n" \
                    f"{push_D}"
        elif segment == "constant":
            asm_code = \
                    f"@{i}\n" \
                    "D=A\n" \
                    f"{push_D}"
        elif segment == "static":
            varname = f"{current_file}.{i}"
            asm_code = \
                    f"@{varname}\n" \
                    "D=M\n" \
                    f"{push_D}"
        elif segment == "temp":
            asm_code = \
                    f"@{5+int(i)}\n" \
                    "D=M\n" \
                    f"{push_D}"
        elif segment == "pointer":
            if int(i) == 0:
                s = "THIS"
            elif int(i) == 1:
                s = "THAT"
            else:
                raise Exception(f"Pointer segment index can be 0 or 1, not {i}.")
            asm_code = \
                    f"@{s}\n" \
                    "D=M\n" \
                    f"{push_D}"
        else:
            raise Exception(f"Incorrect segment name '{segment}' in push command.")
    elif cmd == "pop":
        if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            varname = segment_map(segment)
            asm_code = \
                    f"@{i}\n" \
                    "D=A\n" \
                    f"@{varname}\n" \
                    "D=D+M\n" \
                    "@R13\n" \
                    "M=D\n" \
                    "@SP\n" \
                    "AM=M-1\n" \
                    "D=M\n" \
                    "@R13\n" \
                    "A=M\n" \
                    "M=D"
        elif segment == "static":
            varname = f"{current_file}.{i}"
            asm_code = \
                    "@SP\n" \
                    "AM=M-1\n" \
                    "D=M\n" \
                    f"@{varname}\n" \
                    "M=D"
        elif segment == "temp":
            asm_code = \
                    "@SP\n" \
                    "AM=M-1\n" \
                    "D=M\n" \
                    f"@{5+int(i)}\n" \
                    "M=D"
        elif segment == "pointer":
            if int(i) == 0:
                varname = "THIS"
            elif int(i) == 1:
                varname = "THAT"
            else:
                raise Exception(f"Pointer segment index can be 0 or 1, not {i}.")
            asm_code = \
                    "@SP\n" \
                    "AM=M-1\n" \
                    "D=M\n" \
                    f"@{varname}\n" \
                    "M=D"
        else:
            raise Exception(f"Incorrect segment name '{segment}' in pop command.")
    else:
        raise Exception(f"Incorrect stack command {cmd}.")

    return asm_code


def c_arithmetic(cmd):
    if cmd == "add":
        asm_code = \
                "@SP\n" \
                "AM=M-1\n" \
                "D=M\n" \
                "@SP\n" \
                "A=M-1\n" \
                "M=D+M"
    elif cmd == "sub":
        asm_code = \
                "@SP\n" \
                "AM=M-1\n" \
                "D=M\n" \
                "@SP\n" \
                "A=M-1\n" \
                "M=M-D"
    elif cmd == "neg":
        asm_code = \
                "@SP\n" \
                "A=M-1\n" \
                "M=-M"
    else:
        raise Exception(f"Incorrect arithmetic command {cmd}.")
    return asm_code


def c_logical(cmd):
    if cmd == "and":
        asm_code = \
                "@SP\n" \
                "AM=M-1\n" \
                "D=M\n" \
                "@SP\n" \
                "A=M-1\n" \
                "M=D&M"
    elif cmd == "or":
        asm_code = \
                "@SP\n" \
                "AM=M-1\n" \
                "D=M\n" \
                "@SP\n" \
                "A=M-1\n" \
                "M=D|M"
    elif cmd == "not":
        asm_code = \
                "@SP\n" \
                "A=M-1\n" \
                "M=!M"
    else:
        raise Exception(f"Incorrect logical command {cmd}.")
    return asm_code


def c_comparison(cmd):
    global eq_counter, gt_counter, lt_counter

    if cmd == "eq":
        eq_counter += 1
        i = eq_counter
    elif cmd == "gt":
        gt_counter += 1
        i = gt_counter
    elif cmd == "lt":
        lt_counter += 1
        i = lt_counter
    else:
        raise Exception(f"Incorrect comparison command {cmd}.")
    cmd = cmd.upper()
    label = f"end{cmd}{i}"
    asm_code = \
            "@SP\n" \
            "AM=M-1\n" \
            "D=M\n" \
            "A=A-1\n" \
            "D=M-D\n" \
            "M=-1\n" \
            f"@{label}\n" \
            f"D;J{cmd}\n" \
            "@SP\n" \
            "A=M-1\n" \
            "M=0\n" \
            f"({label})"
    return asm_code


def c_branching(cmd, label):
    label = f"{current_func}${label}"
    if cmd == "label":
        asm_code = f"({label})"
    elif cmd == "goto":
        asm_code = \
                f"@{label}\n" \
                "0;JMP"
    elif cmd == "if-goto":
        asm_code = \
                "@SP\n" \
                "AM=M-1\n" \
                "D=M\n" \
                f"@{label}\n" \
                "D;JNE"
    else:
        raise Exception(f"Incorrect branching command {cmd}.")
    return asm_code


def c_function(cmd, arg1, arg2):
    global call_count, current_func
    if cmd == "function":
        current_func = arg1
        nvars = int(arg2)
        asm_code = f"({current_func})"
        for i in range(nvars):
            asm_code += '\n' + c_stack("push", "constant", 0)
    elif cmd == "call":
        current_func = arg1
        nargs = int(arg2)
        call_count += 1
        ret_label = f"{current_func}$ret.{call_count}"
        asm_code = \
                f"// Call {current_func} {nargs}\n" \
                "// Save the return address\n" \
                f"@{ret_label}\n" \
                "D=A\n" \
                f"{push_D}\n" \
                "// Save LCL of the caller\n" \
                "@LCL\n" \
                "D=M\n" \
                f"{push_D}\n" \
                "// Save ARG of the caller\n" \
                "@ARG\n" \
                "D=M\n" \
                f"{push_D}\n" \
                "// Save THIS of the caller\n" \
                "@THIS\n" \
                "D=M\n" \
                f"{push_D}\n" \
                "// Save THAT of the caller\n" \
                "@THAT\n" \
                "D=M\n" \
                f"{push_D}\n" \
                "// Reposition LCL\n" \
                "@SP\n" \
                "D=M\n" \
                "@LCL\n" \
                "M=D\n" \
                "// Reposition ARG\n" \
                f"@{5+nargs}\n" \
                "D=D-A\n" \
                "@ARG\n" \
                "M=D\n" \
                "// Transfer control to the called function\n" \
                f"@{current_func}\n" \
                "0;JMP\n" \
                "// Declare a label for the return address\n" \
                f"({ret_label})"
    elif cmd == "return":
        asm_code = \
                "// Return command\n" \
                "// Save the return address to R13\n" \
                "@LCL\n" \
                "D=M\n" \
                "@5\n" \
                "D=D-A\n" \
                "A=D\n" \
                "D=M\n" \
                "@R13\n" \
                "M=D\n" \
                "// Reposition ARG of the caller\n" \
                "@SP\n" \
                "A=M-1\n" \
                "D=M\n" \
                "@ARG\n" \
                "A=M\n" \
                "M=D\n" \
                "// Reposition SP of the caller\n" \
                "D=A+1\n" \
                "@SP\n" \
                "M=D\n" \
                "// Restore THAT of the caller\n" \
                "@LCL\n" \
                "D=M\n" \
                "@R14\n"\
                "AM=D-1\n" \
                "D=M\n" \
                "@THAT\n" \
                "M=D\n" \
                "// Restore THIS of the caller\n" \
                "@R14\n" \
                "AM=M-1\n" \
                "D=M\n" \
                "@THIS\n" \
                "M=D\n" \
                "// Restore ARG of the caller\n" \
                "@R14\n" \
                "AM=M-1\n" \
                "D=M\n" \
                "@ARG\n" \
                "M=D\n" \
                "// Restore LCL of the caller\n" \
                "@R14\n" \
                "AM=M-1\n" \
                "D=M\n" \
                "@LCL\n" \
                "M=D\n" \
                "// Go to return address in the caller's code\n" \
                "@R13\n" \
                "A=M\n" \
                "0;JMP"
    else:
        raise Exception(f"Incorrect function command {cmd}.")
    return asm_code
        

def translate_file(in_filename):
    global current_file
    current_file = basename(in_filename)[:-3]
    f = open(in_filename, 'r')
    asm = ""
    for line in f:
        cmd, arg1, arg2= parse_line(line)
        if cmd:
            match cmd:
                case "push" | "pop":
                    asm_code = c_stack(cmd, arg1, arg2) + '\n'
                case "add" | "sub" | "neg":
                    asm_code = c_arithmetic(cmd) + '\n'
                case "eq" | "gt" | "lt":
                    asm_code = c_comparison(cmd) + '\n'
                case "and" | "or" | "not":
                    asm_code = c_logical(cmd) + '\n'
                case "label" | "goto" | "if-goto":
                    asm_code = c_branching(cmd, arg1) + '\n'
                case "function" | "call" | "return":
                    asm_code = c_function(cmd, arg1, arg2) + '\n'
                case _:
                    raise Exception(f"Command not implemented: {cmd}")
            asm += asm_code
    f.close()
    return asm


def main(path):
    path = os.path.normpath(path)
    if os.path.isdir(path):
        asm = "// Bootstrap code\n" \
              "@256\n" \
              "D=A\n" \
              "@SP\n" \
              "M=D\n"
        asm += c_function("call", "Sys.init", "0") + '\n\n'
        for (root, dirs, files) in os.walk(path):
            for fn in files:
                if fn.endswith(".vm"):
                    in_fn = os.path.join(root, fn)
                    asm += f"// Translation of {fn}\n" + translate_file(in_fn) + "\n"
        out_filename = os.path.join(path, basename(path) + ".asm")
    elif os.path.isfile(path) and path.endswith(".vm"):
        asm = f"// Translation of {basename(path)}\n" + translate_file(path)
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
    path = sys.argv[1]
    main(path)
