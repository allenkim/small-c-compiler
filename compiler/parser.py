#!/usr/bin/env python
"""
Compiler written in Python for a small C-style language
"""
import sys
import os
import mmap

from setup import GLOBALS, TK, TYPE
from scanner import get_token, print_token
from error_handling import scanner_error

def match(token):
    if GLOBALS["CUR_TOKEN"] != token:
        scanner_error("Expected {}, but got {}".format(token, GLOBALS["CUR_TOKEN"]))
    else:
        get_token()

def optional_match(token):
    if GLOBALS["CUR_TOKEN"] == token:
        get_token()

def basic_type_dec():
    basic_type = TYPE.INT
    is_char = False
    if GLOBALS["CUR_TOKEN"] == TK.CHAR:
        get_token()
        basic_type = TYPE.CHAR
        is_char = True
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
    if not is_char:
        optional_match(TK.INT)
    return basic_type


def parse_type_dec():
    type_tuple = None
    if GLOBALS["CUR_TOKEN"] == TK.SIGNED:
        get_token()
        type_tuple = (TYPE.SIGNED, basic_type_dec())
    elif GLOBALS["CUR_TOKEN"] == TK.UNSIGNED:
        get_token()
        type_tuple = (TYPE.UNSIGNED, basic_type_dec())
    else:
        type_tuple = (TYPE.SIGNED, basic_type_dec())
        if type_tuple[1] == TYPE.CHAR:
            type_tuple = (TYPE.UNSIGNED, TYPE.CHAR)
    return type_tuple


def parse_function():
    sign, basic_type = parse_type_dec()
    match(TK.ID)
    match(TK.LPAREN)
    match(TK.RPAREN)
    match(TK.LBRACE)
    while GLOBALS["CUR_TOKEN"] == TK.EOLN:
        match(TK.EOLN)
    match(TK.RBRACE)

def main_loop():
    while True:
        get_token()  # our scanner
        if GLOBALS["CUR_TOKEN"] == TK.EOF:
            break
        elif GLOBALS["CUR_TOKEN"] == TK.EOLN:
            continue
        else:
            parse_function()


def parse_c_program():
    # If empty file, we print error
    if os.stat(GLOBALS["CUR_FILE"]).st_size == 0:
        raise ValueError("\nFile: {}\nCannot compile empty file\n".format(GLOBALS["CUR_FILE"]))

    # Open with mmap
    with open(GLOBALS["CUR_FILE"], "r+b") as f:
        # memory-map the file, size 0 means whole file
        GLOBALS["MMAPPED_FILE"] = mmap.mmap(
            f.fileno(), 0, access=mmap.ACCESS_READ)
        main_loop()
        GLOBALS["MMAPPED_FILE"].close()

