#!/usr/bin/env python
"""
SCC SM - Small C Compiler Stack Machine
"""

import argparse, mmap, struct
from enum import Enum

from setup import OP

# 8 bit addresses and numbers for now
def run(code, debug):
    l = len(code)
    data = {}
    stack = []
    ip = 0
    while ip < l:
        op = code[ip]
        ip += 1
        if op == OP.PUSH.value:
            addr = []
            for _ in range(8):
                addr.append(code[ip])
                ip += 1
            addr = struct.unpack("L",bytes(addr))
            addr = addr[0]
            stack.append(data[addr])
            if debug:
                print("push value in addr {} into stack".format(addr))
        elif op == OP.POP.value:
            addr = []
            for _ in range(8):
                addr.append(code[ip])
                ip += 1
            addr = struct.unpack("L",bytes(addr))
            addr = addr[0]
            elt = stack.pop()
            data[addr] = elt
            if debug:
                print("load {} into addr {}".format(elt,addr))
        elif op == OP.PUSHIL.value:
            val = []
            for _ in range(8):
                val.append(code[ip])
                ip += 1
            val = struct.unpack("l",bytes(val))
            val = val[0]
            stack.append(val)
            if debug:
                print("push {} into stack".format(val))
        elif op == OP.PUSHID.value:
            val = []
            for _ in range(8): 
                val.append(code[ip])
                ip += 1
            val = struct.unpack("d",bytes(val))
            val = val[0]
            stack.append(val)
            if debug:
                print("push {} into stack".format(val))
        elif op == OP.ADD.value:
            a = stack.pop()
            b = stack.pop()
            result = a + b
            stack.append(result)
            if debug:
                print("{} + {} = {}".format(b,a,result))
        elif op == OP.SUB.value:
            a = stack.pop()
            b = stack.pop()
            result = b - a
            stack.append(result)
            if debug:
                print("{} - {} = {}".format(b,a,result))
        elif op == OP.MUL.value:
            a = stack.pop()
            b = stack.pop()
            result = b * a
            stack.append(result)
            if debug:
                print("{} * {} = {}".format(b,a,result))
        elif op == OP.DIV.value:
            a = stack.pop()
            b = stack.pop()
            result = b / a
            if b % a == 0:
                result = int(result)
            stack.append(result)
            if debug:
                print("{} / {} = {}".format(b,a,result))
        elif op == OP.MOD.value:
            a = stack.pop()
            b = stack.pop()
            result = b % a
            stack.append(result)
            if debug:
                print("{} % {} = {}".format(b,a,result))
        elif op == OP.EQ.value:
            a = stack.pop()
            b = stack.pop()
            result = (b == a)
            stack.append(result)
            if debug:
                print("{} == {} = {}".format(b,a,result))
        elif op == OP.NEQ.value:
            a = stack.pop()
            b = stack.pop()
            result = (b != a)
            stack.append(result)
            if debug:
                print("{} != {} = {}".format(b,a,result))
        elif op == OP.LT.value:
            a = stack.pop()
            b = stack.pop()
            result = b < a
            stack.append(result)
            if debug:
                print("{} < {} = {}".format(b,a,result))
        elif op == OP.LTE.value:
            a = stack.pop()
            b = stack.pop()
            result = b <= a
            stack.append(result)
            if debug:
                print("{} <= {} = {}".format(b,a,result))
        elif op == OP.GT.value:
            a = stack.pop()
            b = stack.pop()
            result = b > a
            stack.append(result)
            if debug:
                print("{} > {} = {}".format(b,a,result))
        elif op == OP.GTE.value:
            a = stack.pop()
            b = stack.pop()
            result = b >= a
            stack.append(result)
            if debug:
                print("{} >= {} = {}".format(b,a,result))
        elif op == OP.NOT.value:
            a = stack.pop()
            bval = 0
            if a == 0:
                bval = 1
            stack.append(bval)
            if debug:
                print("!{} = {}".format(a,bval))
        elif op == OP.AND.value:
            a = stack.pop()
            b = stack.pop()
            bval = 1
            if a == 0 or b == 0:
                bval = 0
            stack.append(bval)
            if debug:
                print("{} && {} = {}".format(b,a,bval))
        elif op == OP.OR.value:
            a = stack.pop()
            b = stack.pop()
            bval = 1
            if a == 0 and b == 0:
                bval = 0
            stack.append(bval)
            if debug:
                print("{} || {} = {}".format(b,a,bval))
        elif op == OP.BIT_AND.value:
            a = stack.pop()
            b = stack.pop()
            bval = a & b
            stack.append(bval)
            if debug:
                print("{} & {} = {}".format(b,a,bval))
        elif op == OP.BIT_OR.value:
            a = stack.pop()
            b = stack.pop()
            bval = a | b
            stack.append(bval)
            if debug:
                print("{} | {} = {}".format(b,a,bval))
        elif op == OP.XOR.value:
            a = stack.pop()
            b = stack.pop()
            bval = a ^ b
            stack.append(bval)
            if debug:
                print("{} ^ {} = {}".format(b,a,bval))
        elif op == OP.LSHIFT.value:
            a = stack.pop()
            b = stack.pop()
            bval = b << a
            stack.append(bval)
            if debug:
                print("{} << {} = {}".format(b,a,bval))
        elif op == OP.RSHIFT.value:
            a = stack.pop()
            b = stack.pop()
            bval = b >> a
            stack.append(bval)
            if debug:
                print("{} >> {} = {}".format(b,a,bval))
        elif op == OP.JMP.value:
            addr = []
            for _ in range(8):
                addr.append(code[ip])
                ip += 1
            addr = struct.unpack("L",bytes(addr))
            addr = addr[0]
            ip = addr
        elif op == OP.JFALSE.value:
            addr = []
            for _ in range(8):
                addr.append(code[ip])
                ip += 1
            addr = struct.unpack("L",bytes(addr))
            addr = addr[0]
            bval = stack.pop()
            if not bval:
                ip = addr
        elif op == OP.JTRUE.value:
            addr = []
            for _ in range(8):
                addr.append(code[ip])
                ip += 1
            addr = struct.unpack("L",bytes(addr))
            addr = addr[0]
            bval = stack.pop()
            if bval:
                ip = addr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SCC SM - Small C Compiler Stack Machine")
    parser.add_argument("-v","--verbose", help="verbose execution", action="store_true")
    parser.add_argument("executable", help="executable file to compile")
    args = parser.parse_args()

    f = args.executable 
    with open(f, "r+b") as fh:
        m = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
        ba = bytearray(m)
        run(ba, args.verbose)

