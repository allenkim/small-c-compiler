"""
Scanner for our compiler
"""
from setup import (GLOBALS, TK, KEYWORDS, ARITH_OPERATORS)

curr_char = " "

def print_token():
    """
    Prints the current token
    """
    print("{} - Val: {}".format(GLOBALS["CUR_TOKEN"],
                                GLOBALS["CUR_VALUE"]))

def get_char():
    GLOBALS["CUR_COL"] += 1
    return chr(GLOBALS["MMAPPED_FILE"].read_byte())


def get_token():
    """ Get the next token from the source code
    """
    global curr_char
    # Reinitialize current token variables
    GLOBALS["CUR_VALUE"] = ""

    # If we reach the end of the file, return the EOF token
    if GLOBALS["MMAPPED_FILE"].tell() >= GLOBALS["MMAPPED_FILE"].size():
        GLOBALS["SCAN_P"] = GLOBALS["MMAPPED_FILE"].tell()
        GLOBALS["CUR_TOKEN"] = TK.EOF
        return

    # Checks if character is new line
    if curr_char == '\n':
        GLOBALS["CUR_LINE"] += 1
        GLOBALS["CUR_COL"] = 1
        GLOBALS["CUR_TOKEN"] = TK.EOLN
    # Checks if character is white space (not new line)
    elif curr_char.isspace():
        curr_char = get_char()
        get_token()
    # If the char is alphabetical, then we check if keyword or identifier
    elif curr_char.isalpha():
        while True:
            GLOBALS["CUR_VALUE"] += curr_char
            curr_char = get_char()
            if not curr_char.isalnum():
                break
        if GLOBALS["CUR_VALUE"] in KEYWORDS:
            GLOBALS["CUR_TOKEN"] = KEYWORDS[GLOBALS["CUR_VALUE"]]
        else:
            GLOBALS["CUR_TOKEN"] = TK.ID
    # If the char is numerical or dot, then its a number
    elif curr_char.isdigit() or curr_char == '.':
        in_decimal = True if curr_char == '.' else False
        in_e = False
        while True:
            GLOBALS["CUR_VALUE"] += curr_char
            curr_char = get_char()
            if not curr_char.isdigit():
                if in_decimal:
                    GLOBALS["CUR_VALUE"] = float(GLOBALS["CUR_VALUE"])
                    GLOBALS["CUR_TOKEN"] = TK.FLOATLIT
                    break
                else:
                    if curr_char == '.':
                        in_decimal = True
                        continue
                    else:
                        GLOBALS["CUR_VALUE"] = int(GLOBALS["CUR_VALUE"])
                        GLOBALS["CUR_TOKEN"] = TK.INTLIT
                        break
    # Checks if the character is an operator
    elif curr_char in ARITH_OPERATORS:
        GLOBALS["CUR_TOKEN"] = ARITH_OPERATORS[curr_char]
        curr_char = get_char()
    # Checks parentheses
    elif curr_char == '(':
        curr_char = get_char()
        GLOBALS["CUR_TOKEN"] = TK.LPAREN
    elif curr_char == ')':
        curr_char = get_char()
        GLOBALS["CUR_TOKEN"] = TK.RPAREN
    # If character is an unrecognized token, raise error
    else:
        raise ValueError("Unrecognized token!")

    # Update GLOBALS["SCAN_P"] to match what byte we are looking at
    GLOBALS["SCAN_P"] = GLOBALS["MMAPPED_FILE"].tell()

