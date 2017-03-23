"""
Scanner for our compiler
"""
from setup import GLOBALS, TK, KEYWORDS, OPERATORS
from error_handling import scanner_error

curr_char = " "


def print_token():
    """
    Prints the current token
    """
    print("{} - Val: {}".format(GLOBALS["CUR_TOKEN"],
                                GLOBALS["CUR_VALUE"]))


def get_char():
    """
    Grabs the next character from the file and adds one to column
    """
    GLOBALS["CUR_COL"] += 1
    c = chr(GLOBALS["MMAPPED_FILE"].read_byte())
    GLOBALS["SCAN_P"] = GLOBALS["MMAPPED_FILE"].tell()
    return c


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
        curr_char = get_char()
        return
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
                if in_e:
                    GLOBALS["CUR_VALUE"] = float(GLOBALS["CUR_VALUE"])
                    GLOBALS["CUR_TOKEN"] = TK.FLOATLIT
                    break
                else:
                    if curr_char == 'e' or curr_char == 'E':
                        GLOBALS["CUR_VALUE"] += curr_char
                        in_e = True
                        curr_char = get_char()
                        if curr_char == '-' or curr_char.isdigit():
                            continue
                        else:
                            scanner_error(
                                "Expected integer after " + curr_char)
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
    elif curr_char in OPERATORS["L1"]:
        tmp_str = curr_char
        curr_char = get_char()
        tmp_str += curr_char
        if tmp_str in OPERATORS["L2"]:
            curr_char = get_char()
            tmp_str += curr_char
            if tmp_str in OPERATORS["L3"]:
                GLOBALS["CUR_TOKEN"] = OPERATORS["L3"][tmp_str]
                curr_char = get_char()
            else:
                GLOBALS["CUR_TOKEN"] = OPERATORS["L2"][tmp_str[:-1]]
        else:
            GLOBALS["CUR_TOKEN"] = OPERATORS["L1"][tmp_str[:-1]]
    # If character is an unrecognized token, raise error
    else:
        scanner_error("Unrecognized token: {}".format(curr_char))

