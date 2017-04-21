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
    addr_len = 4
    data = {}
    stack = []
    ip = 0
    while ip < l:
        op = code[ip]
        if op == OP.PUSH.value:
            addr = []
            for _ in range(addr_len):
                ip += 1
                addr.append(code[ip])
            addr = struct.unpack("I",bytes(addr))
            addr = addr[0]
            stack.append(data[addr])
            if debug:
                print("push value in addr {} into stack".format(addr))
        elif op == OP.POP.value:
            addr = []
            for _ in range(addr_len):
                ip += 1
                addr.append(code[ip])
            addr = struct.unpack("I",bytes(addr))
            addr = addr[0]
            elt = stack.pop()
            data[addr] = elt
            if debug:
                print("load {} into addr {}".format(elt,addr))
        elif op == OP.PUSHIL.value:
            val = []
            for _ in range(addr_len):
                ip += 1
                val.append(code[ip])
            val = struct.unpack("i",bytes(val))
            val = val[0]
            stack.append(val)
            if debug:
                print("push {} into stack".format(val))
        elif op == OP.PUSHID.value:
            val = []
            for _ in range(addr_len): 
                ip += 1
                val.append(code[ip])
            val = struct.unpack("f",bytes(val))
            val = val[0]
            stack.append(val)
            if debug:
                print("push {} into stack".format(val))
        elif op == OP.INCR.value:
            addr = []
            for _ in range(addr_len):
                ip += 1
                addr.append(code[ip])
            addr = struct.unpack("I",bytes(addr))
            addr = addr[0]
            data[addr] += 1
            if debug:
                print("addr:{} - data: {} + 1 = {}".format(addr,data[addr]-1,data[addr]))
        elif op == OP.DECR.value:
            addr = []
            for _ in range(addr_len):
                ip += 1
                addr.append(code[ip])
            addr = struct.unpack("I",bytes(addr))
            addr = addr[0]
            data[addr] -= 1
            if debug:
                print("addr:{} - data: {} - 1 = {}".format(addr,data[addr]+1,data[addr]))
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
        elif op == OP.BIT_NOT.value:
            a = stack.pop()
            bval = ~a
            stack.append(bval)
            if debug:
                print("~{} = {}".format(a,bval))
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
            for _ in range(addr_len):
                ip += 1
                addr.append(code[ip])
            addr = struct.unpack("i",bytes(addr))
            addr = addr[0]
            ip += addr
            if debug:
                print("jmp {} bytes".format(addr))
            continue
        elif op == OP.JFALSE.value:
            addr = []
            for _ in range(addr_len):
                ip += 1
                addr.append(code[ip])
            addr = struct.unpack("i",bytes(addr))
            addr = addr[0]
            bval = stack.pop()
            if not bval:
                ip += addr
                if debug:
                    print("jmp {} bytes".format(addr))
                continue
        elif op == OP.JTRUE.value:
            addr = []
            for _ in range(addr_len):
                ip += 1
                addr.append(code[ip])
            addr = struct.unpack("i",bytes(addr))
            addr = addr[0]
            bval = stack.pop()
            if bval:
                ip += addr
                if debug:
                    print("jmp {} bytes".format(addr))
                continue
        elif op == OP.HALT.value:
            if debug:
                print("halt")
            return
        elif op == OP.NOP.value:
            if debug:
                print("nop")
        
        ip += 1

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

