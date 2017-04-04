#!/usr/bin/env python
"""
Compiler written in Python for a small C-style language
"""
import sys
import os
import mmap

from setup import GLOBALS, TK
from scanner import get_token, print_token


def match(token):
    if GLOBALS["CUR_TOKEN"] != token:
        raise ValueError("Expected {}, but got {}".format(
            token, GLOBALS["CUR_TOKEN"]))
    else:
        get_token()

def parse_c_program():
    # If empty file, we print error
    if os.stat(GLOBALS["CUR_FILE"]).st_size == 0:
        raise ValueError("Cannot compile empty file")

    # Open with mmap
    with open(GLOBALS["CUR_FILE"], "r+b") as f:
        # memory-map the file, size 0 means whole file
        GLOBALS["MMAPPED_FILE"] = mmap.mmap(
            f.fileno(), 0, access=mmap.ACCESS_READ)
        while True:
            get_token()  # our scanner
            print_token()  # for debugging purposes
            if GLOBALS["CUR_TOKEN"] == TK.EOF:
                break

        GLOBALS["MMAPPED_FILE"].close()

