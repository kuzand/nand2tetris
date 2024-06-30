import sys


DEST_MAP = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}

COMP_MAP = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "M":   "1110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "!M":  "1110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "-M":  "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

JUMP_MAP = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

class SymbTable:
    def __init__(self):
        self.variable_count = 0
        self.table = {
            "R0":     0,
            "R1":     1,
            "R2":     2,
            "R3":     3,
            "R4":     4,
            "R5":     5,
            "R6":     6,
            "R7":     7,
            "R8":     8,
            "R9":     9,
            "R10":    10,
            "R11":    11,
            "R12":    12,
            "R13":    13,
            "R14":    14,
            "R15":    15,
            "SP":     0,
            "LCL":    1,
            "ARG":    2,
            "THIS":   3,
            "THAT":   4,
            "SCREEN": 16384,
            "KBR":    24576,
        }


def itob(x, length):
    """
    Integer to binary string of given length.
    (Using Python tricks: format(x, f"#0{length+2}b")[2:])
    """
    b = []
    while x > 0:
        if x % 2 == 0:
            b.append('0')
        else:
            b.append('1')
        x = x // 2
    
    for i in range(len(b)//2):
        tmp = b[i]
        b[i] = b[len(b) - 1 - i]
        b[len(b) - 1 - i] = tmp
    
    # pad with zeroes to length
    n = length - len(b)
    return '0'*n + ''.join(b)


def parse_line(line):
    """
    If a line is a comment (starts with //) or is an empty line, then return empty string.
    Otherwise remove inline comments and all white spaces from the line and return it.
    """
    parsed_line = ""
    for c in line:
        if c == "/":
            break
        if c != ' ' and c != '\n':
            parsed_line += c
    return parsed_line


def parse_a_instr(instr, symb_table):
    xxx = instr[1:]
    if ord(xxx[0]) >= 48 and ord(xxx[0]) <= 57:
        return int(xxx)
    else:
        if xxx not in symb_table.table:
            symb_table.table[xxx] = 16 + symb_table.variable_count
            symb_table.variable_count += 1
        return int(symb_table.table[xxx])

    
def parse_c_instr(instr):
    """
    Cases:
        dest=comp
        dest=comp;jump
        comp;jump
    """
    field = ""
    dest = ""
    comp = ""
    jump = ""
    has_jump = False
    for c in instr:
        if c == "=":
            dest = field
            field = ""
            continue
        if c == ";":
            has_jump = True
            comp = field
            field = ""
            continue
        field += c
    
    if has_jump:
        jump = field
    else:
        comp = field

    return [dest, comp, jump]


def assemble(in_filename):
    f_in = open(in_filename, 'r')
    f_out = open(in_filename[:-4] + "_my.hack", 'w') 

    symb_table = SymbTable()
    
    # First pass to determine the labels
    instr_count = 0
    for line in f_in:
        instr = parse_line(line)
        if instr:
            if instr[0] == '(':
                label = ""
                for c in instr[1:]:
                    if c == ')':
                        break
                    else:
                        label += c
                symb_table.table[label] = instr_count
            else:
                instr_count += 1
    f_in.seek(0)

    # Second pass
    bin_code = ""
    for line in f_in:
        bin_instr = ""
        instr = parse_line(line)
        if instr:
            if instr[0] == '@':
                parsed_instr = parse_a_instr(instr, symb_table)
                bin_instr = "0" + itob(parsed_instr, 15) 
            elif instr[0] == '(':
                continue
            else:
                parsed_instr = parse_c_instr(instr)
                dest, comp, jump = parsed_instr
                bin_instr = "111" + COMP_MAP[comp] + DEST_MAP[dest] + JUMP_MAP[jump]
            bin_code += bin_instr + '\n'
    
    f_out.write(bin_code)
    f_in.close
    f_out.close
    print("Done!")        



if  __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".asm"):
        raise Exception(f"Usage: python3 {sys.argv[0]} <in_filename.asm>")
    in_filename = sys.argv[1]
    assemble(in_filename)
