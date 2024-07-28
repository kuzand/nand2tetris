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

class SymbolTable:
    table = {
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
    
    def __init__(self):
        self.variable_count = 0

def itob(x, length):
	return format(x, f"0{length}b")[-length:]

def parse_line(line):
	return line.split('//')[0].replace(' ', '').replace('\t', '').replace('\n', '')

def parse_a_instr(instr, symb_table):
	xxx = instr[1:]
	if xxx.isdigit():
		return int(xxx)
	else:
		if xxx not in symb_table.table:
			symb_table.table[xxx] = 16 + symb_table.variable_count
			symb_table.variable_count += 1
		return symb_table.table[xxx]

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
        elif c == ";":
            has_jump = True
            comp = field
            field = ""
        else:
        	field += c
    
    if has_jump:
        jump = field
    else:
        comp = field

    return [dest, comp, jump]

def assemble(in_filename):
    f_in = open(in_filename, 'r')

    symb_table = SymbolTable()
    
    # First pass to determine the labels
    instr_count = 0
    for line in f_in:
        instr = parse_line(line)
        if instr:
            if instr[0] == '(':
                label = instr[1:-1]
                symb_table.table[label] = instr_count
            else:
                instr_count += 1
                
    # Second pass
    f_in.seek(0)
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
                dest, comp, jump = parse_c_instr(instr)
                bin_instr = "111" + COMP_MAP[comp] + DEST_MAP[dest] + JUMP_MAP[jump]
            bin_code += bin_instr + '\n'
    
    f_out = open(in_filename.rsplit('.', 1)[0] + "_my.hack", 'w') 
    f_out.write(bin_code)
    
    f_in.close()
    f_out.close()
    print("Done!")        


if  __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".asm"):
        raise Exception(f"Usage: python3 {sys.argv[0]} <in_filename.asm>")
        sys.exit(1)
        
    in_filename = sys.argv[1]
    assemble(in_filename)
