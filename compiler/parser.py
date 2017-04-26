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
from symtable import make_symbol
from ast import (BodyAST,
                 NumberExprAST, 
                 VariableExprAST,
                 UnaryExprAST,
                 BinaryExprAST,
                 CallExprAST,
                 PrototypeAST,
                 FunctionAST,
                 ReturnAST,
                 PrintAST,
                 IfAST,
                 DoWhileAST,
                 WhileAST,
                 ForAST,
                 BreakAST,)


TYPE_TOKENS = [
    TK.SIGNED,
    TK.UNSIGNED,
    TK.CHAR,
    TK.SHORT,
    TK.INT,
    TK.LONG,
    TK.FLOAT,
    TK.DOUBLE,
    TK.VOID,
] 

TYPE_FLAG_TOKENS = [
    TK.CONST,
    TK.VOLATILE,
]

TYPE_STORAGE_TOKENS = [
    TK.AUTO,
    TK.REGISTER,
    TK.STATIC,
    TK.EXTERN,
]


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

def is_no_semicolon_ast(ast):
    NO_SEMICOLON_AST = [
        FunctionAST, 
        IfAST,
        WhileAST,
        ForAST,
    ]
    for check_ast in NO_SEMICOLON_AST:
        if type(ast) is check_ast:
            return True
    return False


def is_decl_token():
    DECL_TOKENS = TYPE_TOKENS + TYPE_FLAG_TOKENS + TYPE_STORAGE_TOKENS
    return GLOBALS["CUR_TOKEN"] in DECL_TOKENS

def is_typemod_token():
    TYPEMOD_TOKENS = TYPE_FLAG_TOKENS + TYPE_STORAGE_TOKENS
    return GLOBALS["CUR_TOKEN"] in TYPEMOD_TOKENS

def is_prepost_token():
    TYPE_PREPOST_TOKENS = [
        TK.INCR,
        TK.DECR,
    ]
    return GLOBALS["CUR_TOKEN"] in TYPE_PREPOST_TOKENS

def basic_type_dec():
    basic_type = TYPE.INT
    ending_int = True
    if GLOBALS["CUR_TOKEN"] == TK.CHAR:
        get_token()
        basic_type = TYPE.CHAR
        ending_int = False
    elif GLOBALS["CUR_TOKEN"] == TK.SHORT:
        get_token()
        basic_type = TYPE.SHORT
    elif GLOBALS["CUR_TOKEN"] == TK.INT:
        get_token()
        basic_type = TYPE.INT
        ending_int = False
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
    if ending_int:
        optional_match(TK.INT)
    return basic_type

def parse_type_flags():
    flags = set()
    storage = None
    while is_typemod_token():
        if GLOBALS["CUR_TOKEN"] in TYPE_FLAG_TOKENS:
            flags.add(GLOBALS["CUR_TOKEN"])
        elif GLOBALS["CUR_TOKEN"] in TYPE_STORAGE_TOKENS:
            if storage:
                processing_error("multiple storage classes in declaration")
            flags.add(GLOBALS["CUR_TOKEN"])
            storage = GLOBALS["CUR_TOKEN"]
        get_token()
    return list(flags)


def parse_type_dec():
    # (TYPE, True/False) for signed
    type_tuple = None
    if GLOBALS["CUR_TOKEN"] == TK.SIGNED:
        get_token()
        type_tuple = (basic_type_dec(), True)
    elif GLOBALS["CUR_TOKEN"] == TK.UNSIGNED:
        get_token()
        type_tuple = (basic_type_dec(), False)
    elif GLOBALS["CUR_TOKEN"] == TK.VOID:
        get_token()
        type_tuple = (TYPE.VOID, None)
    else:
        type_tuple = (basic_type_dec(), True)
        if type_tuple[0] == TYPE.CHAR:
            type_tuple = (TYPE.CHAR, False)
        elif type_tuple[0] == TYPE.FLOAT:
            type_tuple = (TYPE.FLOAT, None)
        elif type_tuple[0] == TYPE.DOUBLE:
            type_tuple = (TYPE.DOUBLE, None)
    return type_tuple


def parse_id_decl(proto=False):
    flags = []
    if is_typemod_token():
        flags = parse_type_flags()
    typ, signed = parse_type_dec()
    id_name = GLOBALS["CUR_VALUE"]
    match(TK.ID)

    # check if it is a variable
    if GLOBALS["CUR_TOKEN"] != TK.LPAREN:
        if typ == TYPE.VOID:
            processing_error("variable '{}' declared void".format(id_name))
        symb = make_symbol(id_name, TK.VAR, flags, typ, signed)
        GLOBALS["SYMBOL_TABLE"].insert_symbol(symb)
        return VariableExprAST(symb,True)

    # else it is a function prototype
    symb = GLOBALS["SYMBOL_TABLE"].lookup(id_name)
    if not symb:
        symb = GLOBALS["SYMBOL_TABLE"].insert(id_name, TK.FUNC, flags, typ, signed)
    proto = parse_prototype(symb)
    if GLOBALS["CUR_TOKEN"] == TK.SEMICOLON:
        get_token()
        return proto
    match(TK.LBRACE)
    GLOBALS["SYMBOL_TABLE"].enter_scope()
    for arg in proto.args:
        GLOBALS["SYMBOL_TABLE"].insert_symbol(arg.symb)
    body = parse_body()
    match(TK.RBRACE)
    GLOBALS["SYMBOL_TABLE"].exit_scope()
    return FunctionAST(proto, body)


def parse_id_expr():
    id_name = GLOBALS["CUR_VALUE"]
    match(TK.ID)

    # check if it is a variable
    if GLOBALS["CUR_TOKEN"] != TK.LPAREN:
        sym = GLOBALS["SYMBOL_TABLE"].lookup(id_name)
        if sym:
            var_ast = VariableExprAST(sym)
            # check for postfix operators
            if is_prepost_token():
                postfix_op = GLOBALS["CUR_TOKEN"]
                get_token()
                return UnaryExprAST(postfix_op, var_ast, True)
            else:
                return var_ast
        else:
            processing_error("'{}' undeclared".format(id_name))

    # else it is a function call
    match(TK.LPAREN)
    args = []
    if GLOBALS["CUR_TOKEN"] != TK.RPAREN:
        while True:
            arg = parse_expression()
            args.append(arg)
            if GLOBALS["CUR_TOKEN"] != TK.RPAREN:
                match(TK.COMMA)
            else:
                break
    match(TK.RPAREN)
    return CallExprAST(id_name, args)


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
    elif cur_tok == TK.PRINT:
        return parse_print_expression()
    elif cur_tok == TK.IF:
        return parse_if_expression()
    elif cur_tok == TK.DO:
        return parse_do_while_expression()
    elif cur_tok == TK.WHILE:
        return parse_while_expression()
    elif cur_tok == TK.FOR:
        return parse_for_expression()
    elif cur_tok == TK.RETURN:
        return parse_return_expression()
    elif cur_tok == TK.BREAK:
        return parse_break_expression()
    else:
        return None

# Handling binary operation precedence

def get_token_precedence():
    cur_tok = GLOBALS["CUR_TOKEN"]
    if cur_tok in GLOBALS["BINOP_PRECEDENCE"]:
        return GLOBALS["BINOP_PRECEDENCE"][cur_tok]
    else: 
        return -1

def parse_expression():
    lhs = parse_unary()
    if not lhs:
        return None
    bin_expr = parse_binop_rhs(0, lhs)
    return bin_expr

def parse_unary():
    UNARY_OPERATORS = [
        TK.NOT,
        TK.BIT_NOT,
        TK.INCR,
        TK.DECR,
    ]
    if GLOBALS["CUR_TOKEN"] not in UNARY_OPERATORS:
        return parse_primary()
    else:
        prefix_op = GLOBALS["CUR_TOKEN"]
        if is_prepost_token():
            get_token()
            var_ast = parse_id_expr()
            if type(var_ast) is VariableExprAST:
                return UnaryExprAST(prefix_op, var_ast)
            else:
                processing_error("Expected variable after {}".format(prefix_op))
       
        get_token()
        operand = parse_unary()
        if operand:
            return UnaryExprAST(prefix_op, operand)
        return None


def parse_binop_rhs(expr_prec, lhs):
    while True:
        tok_prec = get_token_precedence()
        if tok_prec < expr_prec:
            return lhs

        binop = GLOBALS["CUR_TOKEN"]
        get_token()
        rhs = parse_unary()
        if not rhs:
            return None

        next_prec = get_token_precedence()

        if tok_prec < next_prec:
            # a binop (b binop unparsed) in this case
            rhs = parse_binop_rhs(expr_prec+1, rhs)
            if not rhs:
                return None

        lhs = BinaryExprAST(binop, lhs, rhs)

def parse_prototype(symb):
    match(TK.LPAREN)
    arg_names = []
    while is_decl_token():
        expr = parse_id_decl()
        arg_names.append(expr)
        if GLOBALS["CUR_TOKEN"] == TK.RPAREN:
            break
        match(TK.COMMA)
    match(TK.RPAREN)
    return PrototypeAST(symb, arg_names)

def parse_return_expression():
    match(TK.RETURN)
    expr = parse_expression()
    return ReturnAST(expr)

def parse_print_expression():
    match(TK.PRINT)
    match(TK.LPAREN)
    expr = parse_expression()
    match(TK.RPAREN)
    return PrintAST(expr)

def parse_break_expression():
    match(TK.BREAK)
    return BreakAST()

def parse_if_expression():
    match(TK.IF)
    match(TK.LPAREN)
    cond = parse_expression()
    match(TK.RPAREN)

    body = None
    if GLOBALS["CUR_TOKEN"] == TK.LBRACE:
        match(TK.LBRACE)
        GLOBALS["SYMBOL_TABLE"].enter_scope()
        body = parse_body()
        match(TK.RBRACE)
        GLOBALS["SYMBOL_TABLE"].exit_scope()
    else:
        body = parse_expression()
        match(TK.SEMICOLON)
        
    els = None
    if GLOBALS["CUR_TOKEN"] == TK.ELSE:
        match(TK.ELSE)
        if GLOBALS["CUR_TOKEN"] == TK.LBRACE:
            match(TK.LBRACE)
            GLOBALS["SYMBOL_TABLE"].enter_scope()
            els = parse_body()
            match(TK.RBRACE)
            GLOBALS["SYMBOL_TABLE"].exit_scope()
        elif GLOBALS["CUR_TOKEN"] == TK.IF:
            els = parse_if_expression()
        else:
            els = parse_expression()
            match(TK.SEMICOLON)
    return IfAST(cond, body, els)

def parse_do_while_expression():
    match(TK.DO)
    body = None
    if GLOBALS["CUR_TOKEN"] == TK.LBRACE:
        match(TK.LBRACE)
        GLOBALS["SYMBOL_TABLE"].enter_scope()
        body = parse_body()
        match(TK.RBRACE)
        GLOBALS["SYMBOL_TABLE"].exit_scope()
    else:
        body = parse_expression()
        match(TK.SEMICOLON)

    match(TK.WHILE)
    match(TK.LPAREN)
    cond = parse_expression()
    match(TK.RPAREN)
    return DoWhileAST(body,cond)

def parse_while_expression():
    match(TK.WHILE)
    match(TK.LPAREN)
    cond = parse_expression()
    match(TK.RPAREN)
    body = None
    if GLOBALS["CUR_TOKEN"] == TK.LBRACE:
        match(TK.LBRACE)
        GLOBALS["SYMBOL_TABLE"].enter_scope()
        body = parse_body()
        match(TK.RBRACE)
        GLOBALS["SYMBOL_TABLE"].exit_scope()
    else:
        body = parse_expression()
        match(TK.SEMICOLON)
    return WhileAST(cond,body)

def parse_for_expression():
    match(TK.FOR)
    match(TK.LPAREN)
    init = None
    if is_decl_token():
        init = parse_id_decl()
        if type(init) is VariableExprAST and GLOBALS["CUR_TOKEN"] == TK.ASSIGNMENT:
            init = parse_binop_rhs(0, init)
    else:
        init = parse_expression()
    match(TK.SEMICOLON)
    cond = parse_expression()
    match(TK.SEMICOLON)
    update = parse_expression()
    match(TK.RPAREN)
    body = None
    if GLOBALS["CUR_TOKEN"] == TK.LBRACE:
        match(TK.LBRACE)
        GLOBALS["SYMBOL_TABLE"].enter_scope()
        body = parse_body()
        match(TK.RBRACE)
        GLOBALS["SYMBOL_TABLE"].exit_scope()
    else:
        body = parse_expression()
        match(TK.SEMICOLON)
    return ForAST(init,cond,update,body)


def parse_body():
    body = BodyAST()
    lbrace_num = 0
    while GLOBALS["CUR_TOKEN"] != TK.RBRACE or lbrace_num > 0:
        if is_decl_token():
            lhs = parse_id_decl()
            if type(lhs) is VariableExprAST and GLOBALS["CUR_TOKEN"] == TK.ASSIGNMENT:
                expr = parse_binop_rhs(0, lhs)
                match(TK.SEMICOLON)
                body.insert(expr)
            else:
                match(TK.SEMICOLON)
                body.insert(lhs)
        elif GLOBALS["CUR_TOKEN"] == TK.LBRACE:
            match(TK.LBRACE)
            lbrace_num += 1
            GLOBALS["SYMBOL_TABLE"].enter_scope()
        elif GLOBALS["CUR_TOKEN"] == TK.RBRACE:
            match(TK.RBRACE)
            lbrace_num -= 1
            GLOBALS["SYMBOL_TABLE"].exit_scope()
        else:
            expr = parse_expression()
            if not is_no_semicolon_ast(expr):
                match(TK.SEMICOLON)
            body.insert(expr)
    return body

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
        GLOBALS["MMAPPED_FILE"].close()
        return ast

