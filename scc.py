#!/usr/bin/env python
"""
Compiler written in Python for a small C-style language
"""
import sys

from setup import GLOBALS
from parser import parse_c_program


if __name__ == "__main__":
    # First check that we got an input file
    if len(sys.argv) < 2:
        raise ImportError("Expected input file")

    GLOBALS["CUR_FILE"] = sys.argv[1]

    parse_c_program()
