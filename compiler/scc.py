#!/usr/bin/env python
"""
Compiler written in Python for a small C-style language
"""
import sys, argparse, struct

from setup import GLOBALS, TK, OP
from symtable import SymbolTable
from parser import parse_c_program

# sys.tracebacklimit = None

WORD_TO_OP = {
    "push": OP.PUSH,
    "pushil": OP.PUSHIL,
    "pushid": OP.PUSHID,
    "pop": OP.POP,
    "add": OP.ADD,
    "sub": OP.SUB,
    "mul": OP.MUL,
    "div": OP.DIV,
    "mod": OP.MOD,
    "incr": OP.INCR,
    "decr": OP.DECR,
    "eq": OP.EQ,
    "neq": OP.NEQ,
    "lt": OP.LT,
    "lte": OP.LTE,
    "gt": OP.GT,
    "gte": OP.GTE,
    "not": OP.NOT,
    "and": OP.AND,
    "or": OP.OR,
    "bitnot": OP.BIT_NOT,
    "bitand": OP.BIT_AND,
    "bitor": OP.BIT_OR,
    "xor": OP.XOR,
    "shl": OP.LSHIFT,
    "shr": OP.RSHIFT,
    "jmp": OP.JMP,
    "jfalse": OP.JFALSE,
    "jtrue": OP.JTRUE,
    "halt": OP.HALT,
    "nop": OP.NOP,
}

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def assembly_to_bytes(assembly):
    words = assembly.split()
    addr_len = 4
    bytewords = []
    for word in words:
        if word in WORD_TO_OP:
            bytewords.append(bytes([WORD_TO_OP[word].value])) 
        elif word.isdigit(): 
            bytewords.append(struct.pack("i",int(word)))
            for _ in range(addr_len-1):
                bytewords.append("filler")
        elif isfloat(word):
            bytewords.append(struct.pack("f",float(word)))
            for _ in range(addr_len-1):
                bytewords.append("filler")
        elif ":" in word:
            bytewords.append(word)
        elif "L" in word:
            for _ in range(addr_len-1):
                bytewords.append("filler")
            bytewords.append(word)
        else:
            raise ValueError("Unexpected word '{}'".format(word))

    label_addr = {}
    label_holes = {}
    for idx, word in enumerate(bytewords):
        if isinstance(word,bytes) or word == "filler":
            continue
        elif ":" in word:
            num = int(word[1:-1])
            label_addr[num] = idx
        elif "L" in word:
            num = int(word[1:])
            if num in label_holes:
                label_holes[num].append(idx)
            else:
                label_holes[num] = [idx]

    for label_num in label_holes:
        for idx in label_holes[label_num]:
            addr = label_addr[label_num]
            bytewords[idx] = struct.pack("i",addr - idx)

    bytewords = [byte for byte in bytewords if byte != "filler" and byte[0] != "L"]
    return b''.join(bytewords)

def init_binop_map():
    GLOBALS["SYMBOL_TABLE"] = SymbolTable()

    GLOBALS["BINOP_PRECEDENCE"][TK.COMMA] = 10

    GLOBALS["BINOP_PRECEDENCE"][TK.ASSIGNMENT] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.PLUS_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.MINUS_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.MUL_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.DIV_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.MOD_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.BIT_AND_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.BIT_OR_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.BIT_XOR_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.LSHIFT_EQ] = 20
    GLOBALS["BINOP_PRECEDENCE"][TK.RSHIFT_EQ] = 20

    GLOBALS["BINOP_PRECEDENCE"][TK.OR] = 30

    GLOBALS["BINOP_PRECEDENCE"][TK.AND] = 40

    GLOBALS["BINOP_PRECEDENCE"][TK.BIT_OR] = 50

    GLOBALS["BINOP_PRECEDENCE"][TK.BIT_XOR] = 60

    GLOBALS["BINOP_PRECEDENCE"][TK.BIT_AND] = 70

    GLOBALS["BINOP_PRECEDENCE"][TK.EQ] = 80
    GLOBALS["BINOP_PRECEDENCE"][TK.NEQ] = 80

    GLOBALS["BINOP_PRECEDENCE"][TK.LT] = 90
    GLOBALS["BINOP_PRECEDENCE"][TK.LTE] = 90
    GLOBALS["BINOP_PRECEDENCE"][TK.GT] = 90
    GLOBALS["BINOP_PRECEDENCE"][TK.GTE] = 90

    GLOBALS["BINOP_PRECEDENCE"][TK.LSHIFT] = 100
    GLOBALS["BINOP_PRECEDENCE"][TK.RSHIFT] = 100
    
    GLOBALS["BINOP_PRECEDENCE"][TK.PLUS] = 110
    GLOBALS["BINOP_PRECEDENCE"][TK.MINUS] = 110

    GLOBALS["BINOP_PRECEDENCE"][TK.MUL] = 120
    GLOBALS["BINOP_PRECEDENCE"][TK.DIV] = 120
    GLOBALS["BINOP_PRECEDENCE"][TK.MOD] = 120


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SCC - Small C Compiler")
    parser.add_argument("-S", help="output assembly", action="store_true")
    parser.add_argument("-o","--outfile", help="output executable name")
    parser.add_argument("infile", help="input file to compile")
    args = parser.parse_args()

    GLOBALS["CUR_FILE"] = args.infile

    init_binop_map()

    path, suffix = args.infile.split('.',1)
    name = path.split('/')[-1]

    if suffix != 'c' and suffix != 's':
        raise ValueError("Unrecognized suffix '{}'".format(suffix))

    if suffix == 's':
        f = "a.out"
        if args.outfile:
            f = args.outfile
        with open(args.infile,"r") as infile:
            bytecode = assembly_to_bytes(infile.read())
            with open(f,"wb") as fh:
                fh.write(bytecode)
        sys.exit()
 
    ast = parse_c_program()
    ast.print()

    assembly = ast.generate_assembly()

    if args.S:
        f = name + ".s"
        if args.outfile:
            f = args.outfile
        with open(f,"w") as fh:
            fh.write(assembly)
    else:
        f = "a.out"
        if args.outfile:
            f = args.outfile
        bytecode = assembly_to_bytes(assembly)
        with open(f,"wb") as fh:
            fh.write(bytecode)
 
