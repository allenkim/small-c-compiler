#!/usr/bin/env python
"""
Compiler written in Python for a small C-style language
"""
import sys
import os
import mmap

from setup import GLOBALS, TK, TYPE
from scanner import get_token, print_token

def match(token):
    if GLOBALS["CUR_TOKEN"] != token:
        raise ValueError("Expected {}, but got {}".format(
            token, GLOBALS["CUR_TOKEN"]))
    else:
        get_token()

def optional_match(token):
    if GLOBALS["CUR_TOKEN"] == token:
        get_token()

def basic_type_dec():
    basic_type = None
    if GLOBALS["CUR_TOKEN"] == TK.CHAR:
        get_token()
        basic_type = TYPE.CHAR
    elif GLOBALS["CUR_TOKEN"] == TK.SHORT:
        get_token()
        basic_type = TYPE.SHORT
    elif GLOBALS["CUR_TOKEN"] == TK.INT:
        get_token()
        basic_type = TYPE.INT
    elif GLOBALS["CUR_TOKEN"] == TK.LONG:
        get_token()
        optional_match(TK.LONG)
        basic_type = TYPE.LONG
    elif GLOBALS["CUR_TOKEN"] == TK.FLOAT:
        get_token()
        basic_type = TYPE.FLOAT
    elif GLOBALS["CUR_TOKEN"] == TK.DOUBLE:
        get_token()
        basic_type = TYPE.DOUBLE
    optional_match(TK.INT)
    return basic_type


def type_dec():
    type_tuple = None
    if GLOBALS["CUR_TOKEN"] == TK.SIGNED:
        type_tuple = (TYPE.SIGNED, basic_type_dec())
    elif GLOBALS["CUR_TOKEN"] == TK.UNSIGNED:
        type_tuple = (TYPE.UNSIGNED, basic_type_dec())
    else:
        type_tuple = (TYPE.SIGNED, basic_type_dec())
        if type_tuple[1] == TYPE.CHAR:
            type_tuple[0] = TYPE.UNSIGNED
    return type_tuple

def main_loop():
    while True:
        get_token()  # our scanner
        if GLOBALS["CUR_TOKEN"] == TK.EOF:
            break

    
def parse_c_program():
    # If empty file, we print error
    if os.stat(GLOBALS["CUR_FILE"]).st_size == 0:
        raise ValueError("Cannot compile empty file")

    # Open with mmap
    with open(GLOBALS["CUR_FILE"], "r+b") as f:
        # memory-map the file, size 0 means whole file
        GLOBALS["MMAPPED_FILE"] = mmap.mmap(
            f.fileno(), 0, access=mmap.ACCESS_READ)
        main_loop()
        GLOBALS["MMAPPED_FILE"].close()

