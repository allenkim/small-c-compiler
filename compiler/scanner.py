"""
Scanner for our compiler
"""
from setup import GLOBALS, TK, KEYWORDS, OPERATORS
from error_handling import processing_error

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
    if GLOBALS["MMAPPED_FILE"].tell() >= GLOBALS["MMAPPED_FILE"].size():
        return TK.EOF

    GLOBALS["CUR_COL"] += 1
    c = chr(GLOBALS["MMAPPED_FILE"].read_byte())

    if c == '\n':
        GLOBALS["CUR_LINE"] += 1
        GLOBALS["CUR_COL"] = 1
 
    GLOBALS["SCAN_P"] = GLOBALS["MMAPPED_FILE"].tell()
    return c

def get_token():
    """ Get the next token from the source code
    """
    global curr_char
    # Reinitialize current token variables
    GLOBALS["CUR_VALUE"] = ""

    # Check for end of file
    if curr_char == TK.EOF:
        GLOBALS["CUR_TOKEN"] = TK.EOF
        return
    
    # Checks if character is white space
    # New line is treated as a special case though
    while curr_char.isspace():
        if curr_char == '\n':
            GLOBALS["CUR_TOKEN"] = TK.EOLN
            curr_char = get_char()
            return
        curr_char = get_char()

    # If the char is alphabetical or underscore, then we check if keyword or identifier
    if curr_char.isalpha() or curr_char == '_':
        while True:
            GLOBALS["CUR_VALUE"] += curr_char
            curr_char = get_char()
            if not (curr_char.isalnum() or curr_char == '_'):
                break
        if GLOBALS["CUR_VALUE"] in KEYWORDS:
            GLOBALS["CUR_TOKEN"] = KEYWORDS[GLOBALS["CUR_VALUE"]]
        else:
            GLOBALS["CUR_TOKEN"] = TK.ID
    # If the char is numerical or dot, then its a number
    # Also handle e/E in numbers
    elif curr_char.isdigit() or curr_char == '.':
        in_decimal = True if curr_char == '.' else False
        in_e = False
        while True:
            GLOBALS["CUR_VALUE"] += curr_char
            curr_char = get_char()
            if not curr_char.isdigit():
                if in_e:
                    GLOBALS["CUR_VALUE"] = float(GLOBALS["CUR_VALUE"])
                    GLOBALS["CUR_TOKEN"] = TK.DOUBLELIT
                    break
                else:
                    if curr_char == 'e' or curr_char == 'E':
                        GLOBALS["CUR_VALUE"] += curr_char
                        in_e = True
                        curr_char = get_char()
                        if curr_char == '-' or curr_char.isdigit():
                            continue
                        else:
                            processing_error(
                                "Expected integer after " + curr_char)
                if in_decimal:
                    GLOBALS["CUR_VALUE"] = float(GLOBALS["CUR_VALUE"])
                    GLOBALS["CUR_TOKEN"] = TK.DOUBLELIT
                    break
                else:
                    if curr_char == '.':
                        in_decimal = True
                        continue
                    else:
                        GLOBALS["CUR_VALUE"] = int(GLOBALS["CUR_VALUE"])
                        GLOBALS["CUR_TOKEN"] = TK.INTLIT
                        break
    # Handle line and multiline comments
    elif curr_char == '/':
        curr_char = get_char()
        if curr_char == '/':
            while curr_char != '\n':
                curr_char = get_char()
            if curr_char != TK.EOF:
                get_token()
        elif curr_char == '*':
            while True:
                curr_char = get_char()
                if curr_char == '*':
                    curr_char = get_char()
                    if curr_char == '/':
                        curr_char = get_char()
                        get_token()
                        break
                elif curr_char == TK.EOF:
                    processing_error("Unterminated comment")
    # Handle characters
    elif curr_char == '\'':
        GLOBALS["CUR_VALUE"] = 0
        while True:
            curr_char = get_char()
            if curr_char == '\'':
                GLOBALS["CUR_TOKEN"] = TK.INTLIT
                curr_char = get_char()
                break
            elif curr_char == '\n' or curr_char == TK.EOF:
                processing_error("Unterminated character string")
            else:
                GLOBALS["CUR_VALUE"] <<= 8
                GLOBALS["CUR_VALUE"] += ord(curr_char)
    # Handle string literals
    elif curr_char == '"':
        while True:
            curr_char = get_char()
            if curr_char == '"':
                GLOBALS["CUR_TOKEN"] = TK.STRINGLIT
                curr_char = get_char()
                break
            elif curr_char == '\n' or curr_char == TK.EOF:
                processing_error("Unterminated string literal")
            else:
                GLOBALS["CUR_VALUE"] += curr_char
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
        processing_error("Unrecognized token: {}".format(curr_char))

