#!/usr/bin/env python
"""
Compiler written in Python for a small C-style language
"""
import sys

from setup import GLOBALS
from parser import parse_c_program

sys.tracebacklimit = None

if __name__ == "__main__":
    # First check that we got an input file
    if len(sys.argv) < 2:
        raise ImportError("\nExpected input file\n")

    GLOBALS["CUR_FILE"] = sys.argv[1]

    parse_c_program()
