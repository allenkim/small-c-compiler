"""
Compiler written in Python for a small C-style language
"""

import sys
import mmap
from enum import Enum, auto

#########################
# GLOBAL VARIABLE SETUP #
#########################


class TK(Enum):
    """
    Enumeration of all the different tokens available in the language
    """
    # Types
    INTLIT = auto()
    FLOATLIT = auto()
    STRING = auto()
    ID = auto()

    # Keywords
    INT = auto()
    FLOAT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    DO = auto()
    FOR = auto()
    BREAK = auto()
    CONTINUE = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()
    EQ = auto()
    NEQ = auto()

    # Groupers
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()

    # End of line and end of file
    EOLN = auto()
    EOF = auto()

KEYWORDS = {
    "int": TK.INT,
    "float": TK.FLOAT,
    "if": TK.IF,
    "else": TK.ELSE,
    "while": TK.WHILE,
    "do": TK.DO,
    "for": TK.FOR,
    "break": TK.BREAK,
    "continue": TK.CONTINUE
}

CUR_TOKEN = None
CUR_VALUE = None
CUR_NAME = ""

CUR_FILE = ""
CUR_LINE = 0
CUR_COL = 0
SCAN_P = 0

MMAPPED_FILE = None

####################
# OUR SCANNER CODE #
####################


def get_token():
    """
    Get the next token from the source code
    """
    global CUR_TOKEN, CUR_VALUE, CUR_NAME, SCAN_P
    # If we reach the end of the file, return the EOF token
    if MMAPPED_FILE.tell() > MMAPPED_FILE.size():
        return TK.EOF

    curr_char = chr(MMAPPED_FILE.read_byte())

    # If the char is alphabetical, then we check if keyword or identifier
    if curr_char.isalpha():
        while True:
            CUR_NAME += curr_char
            curr_char = chr(MMAPPED_FILE.read_byte())
            if not curr_char.isalnum():
                break
        if CUR_NAME in KEYWORDS:
            return KEYWORDS[CUR_NAME]
        else:
            return TK.ID
    elif curr_char.isdigit() or curr_char == '.':
        in_decimal = True if curr_char == '.' else False
        while True:
            CUR_NAME += curr_char
            curr_char = chr(MMAPPED_FILE.read_byte())
            if in_decimal and not curr_char.isdigit():
                CUR_VALUE = float(CUR_NAME)
                CUR_TOKEN = TK.FLOATLIT
            elif not in_decimal and not curr_char.isdigit():
                if curr_char == '.':
                    in_decimal = True
                    continue
                else:
                    CUR_VALUE = int(CUR_NAME)
                    CUR_TOKEN = TK.INTLIT

    # Update SCAN_P to match what byte we are looking at
    SCAN_P = MMAPPED_FILE.tell()


def print_token():
    """
    Prints the current token
    """
    print(CUR_TOKEN)

##########################
# OUR MAIN COMPILER CODE #
##########################
if __name__ == "__main__":
    # First check that we got an input file
    if len(sys.argv) < 2:
        raise ImportError("Expected input file")

    # Then we open with mmap
    with open(sys.argv[1], "r+b") as f:
        # memory-map the file, size 0 means whole file
        MMAPPED_FILE = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        while True:
            get_token()  # our scanner
            print_token()  # for debugging purposes
            if CUR_TOKEN == TK.EOF:
                break

        MMAPPED_FILE.close()
