#!/usr/bin/env python
"""
Compiler written in Python for a small C-style language
"""
import sys
import os
import mmap

from setup import GLOBALS, TK, TYPE
from scanner import get_token, print_token
from error_handling import processing_error
from ast import (BodyAST,
                 NumberExprAST, 
                 VariableExprAST,
                 BinaryExprAST,
                 CallExprAST,
                 PrototypeAST,
                 FunctionAST)

def match(token):
    if GLOBALS["CUR_TOKEN"] != token:
        processing_error("Expected {}, but got {}".format(token, GLOBALS["CUR_TOKEN"]))
    else:
        get_token()

def optional_match(token):
    if GLOBALS["CUR_TOKEN"] == token:
        get_token()


def parse_number_expr(typ, signed=None):
    result = NumberExprAST(GLOBALS["CUR_VALUE"], typ, signed)
    get_token()
    return result

def parse_paren_expr():
    match(TK.LPAREN)
    v = parse_expression()
    match(TK.RPAREN)
    return v

def is_decl_token():
    decl_tokens = [
        TK.SIGNED,
        TK.UNSIGNED,
        TK.CHAR,
        TK.SHORT,
        TK.INT,
        TK.LONG,
        TK.FLOAT,
        TK.DOUBLE,
    ]
    return GLOBALS["CUR_TOKEN"] in decl_tokens

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
    # (TYPE, True/False) for signed
    type_tuple = None
    if GLOBALS["CUR_TOKEN"] == TK.SIGNED:
        get_token()
        type_tuple = (basic_type_dec(), True)
    elif GLOBALS["CUR_TOKEN"] == TK.UNSIGNED:
        get_token()
        type_tuple = (basic_type_dec(), False)
    else:
        type_tuple = (basic_type_dec(), True)
        if type_tuple[1] == TYPE.CHAR:
            type_tuple = (TYPE.CHAR, False)
    return type_tuple


def parse_id_decl():
    typ, signed = parse_type_dec()
    id_name = GLOBALS["CUR_VALUE"]
    match(TK.ID)

    # check if it is a variable
    if GLOBALS["CUR_TOKEN"] != TK.LPAREN:
        GLOBALS["SYMBOL_TABLE"].insert(id_name, TK.VAR, [], typ, signed)
        return VariableExprAST(id_name, typ, signed)

    # else it is a function prototype
    proto = GLOBALS["SYMBOL_TABLE"].lookup(id_name)
    if not proto:
        proto = parse_prototype(id_name, typ, signed)
        GLOBALS["SYMBOL_TABLE"].insert(id_name, TK.FUNC, [], typ, signed)
    if GLOBALS["CUR_TOKEN"] == TK.SEMICOLON:
        get_token()
        return proto
    match(TK.LBRACE)
    GLOBALS["SYMBOL_TABLE"].start_new_scope()
    body = parse_body()
    match(TK.RBRACE)
    GLOBALS["SYMBOL_TABLE"].close_scope()
    return FunctionAST(proto, body)


def parse_id_expr(typ=None, signed=None):
    id_name = GLOBALS["CUR_VALUE"]
    match(TK.ID)

    # check if it is a variable
    if GLOBALS["CUR_TOKEN"] != TK.LPAREN:
        sym = GLOBALS["SYMBOL_TABLE"].lookup(id_name)
        if sym:
            return VariableExprAST(id_name, sym["type"], sym["signed"])
        else:
            processing_error("'{}' undeclared".format(id_name))

    # else it is a function call
    # at the moment, we don't handle arguments
    match(TK.LPAREN)
    match(TK.RPAREN)
    return CallExprAST(id_name, [])


def parse_primary():
    cur_tok = GLOBALS["CUR_TOKEN"]
    if cur_tok == TK.ID:
        return parse_id_expr()
    elif cur_tok == TK.INTLIT:
        return parse_number_expr(TYPE.INT, signed=None)
    elif cur_tok == TK.DOUBLELIT:
        return parse_number_expr(TYPE.DOUBLE)
    elif cur_tok == TK.LPAREN:
        return parse_paren_expr()
    else:
        return None
        # processing_error("Unexpected token {}  when expecting expression".format(cur_tok))

# Handling binary operation precedence

binop_precedence = GLOBALS["BINOP_PRECEDENCE"]

def get_token_precedence():
    cur_tok = GLOBALS["CUR_TOKEN"]
    if cur_tok in binop_precedence:
        return binop_precedence[cur_tok]
    else: 
        return -1

def parse_body():
    body = BodyAST()
    while GLOBALS["CUR_TOKEN"] != TK.RBRACE:
        expr = parse_expression()
        match(TK.SEMICOLON)
        body.insert(expr)
    return body


def parse_expression():
    if is_decl_token():
        lhs = parse_id_decl()
        if type(lhs) is FunctionAST:
            processing_error("Cannot nest function {} in another function".format(lhs.name))
        if GLOBALS["CUR_TOKEN"] == TK.ASSIGNMENT:
            return parse_binop_rhs(0, lhs)
        else:
            return lhs

    lhs = parse_primary()
    if not lhs:
        return None
    bin_expr = parse_binop_rhs(0, lhs)
    return bin_expr

def parse_binop_rhs(expr_prec, lhs):
    while True:
        tok_prec = get_token_precedence()
        if tok_prec < expr_prec:
            return lhs

        binop = GLOBALS["CUR_TOKEN"]
        get_token()
        rhs = parse_primary()
        if not rhs:
            return None

        next_prec = get_token_precedence()

        if tok_prec < next_prec:
            # a binop (b binop unparsed) in this case
            rhs = parse_binop_rhs(expr_prec+1, rhs)
            if not rhs:
                return None

        lhs = BinaryExprAST(binop, lhs, rhs)

def parse_prototype(fn_name, typ, signed=None):
    match(TK.LPAREN)
    # no arguments allowed for now...
    match(TK.RPAREN)
    return PrototypeAST(fn_name, [], typ, signed)

def main_loop():
    ast = BodyAST()
    while True:
        get_token()  # our scanner
        if GLOBALS["CUR_TOKEN"] == TK.EOF:
            return ast
        else:
            expr = parse_id_decl()
            ast.insert(expr)


def parse_c_program():
    # If empty file, we print error
    if os.stat(GLOBALS["CUR_FILE"]).st_size == 0:
        raise ValueError("\nFile: {}\nCannot compile empty file\n".format(GLOBALS["CUR_FILE"]))

    # Open with mmap
    with open(GLOBALS["CUR_FILE"], "r+b") as f:
        # memory-map the file, size 0 means whole file
        GLOBALS["MMAPPED_FILE"] = mmap.mmap(
            f.fileno(), 0, access=mmap.ACCESS_READ)
        ast = main_loop()
        ast.print()
        GLOBALS["MMAPPED_FILE"].close()

