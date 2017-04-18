#!/usr/bin/env python
"""
Compiler written in Python for a small C-style language
"""
import sys, argparse

from setup import GLOBALS
from symtable import SymbolTable
from parser import parse_c_program

# sys.tracebacklimit = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SCC - Small C Compiler")
    parser.add_argument("-S", help="output assembly", action="store_true")
    parser.add_argument("-o","--outfile", help="output executable name")
    parser.add_argument("infile", help="input file to compile")
    args = parser.parse_args()

    GLOBALS["CUR_FILE"] = args.infile
    if args.outfile:
        print(args.outfile)
    if args.S:
        print("writing to {}.s".format(args.infile.split('.')[0]))

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

    parse_c_program()
