"""
Setup of global variables
"""
from enum import Enum, auto

class TK(Enum):
    """
    Enumeration of all the different tokens available in the language
    """
    # Literals or Identifiers
    INTLIT = auto()  # -2^31, -2^31 + 1, ..., -1, 0, 1, ..., 2^31 - 1
    FLOATLIT = auto()  # 0.0, 1.2, 3.0 / 2, ...
    STRINGLIT = auto()  # "hello", "world", ...
    ID = auto()  # a, abc, ab123, ...

    # Types
    SIGNED = auto() # either prefix or interpreted as int
    UNSIGNED = auto() # either prefix or interpreted as unsigned int
    CHAR = auto() # 1 byte (unsigned)
    SHORT = auto() # either prefix (short int) or 2 bytes (signed short)
    INT = auto() # 4 bytes (signed)
    LONG = auto() # either prefix (long long, ...)  or 8 bytes (signed long)
    FLOAT = auto() # 4 bytes
    DOUBLE = auto() # 8 bytes

    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    DO = auto()
    FOR = auto()
    BREAK = auto()
    CONTINUE = auto()
    VOID = auto()

    # Arithmetic Operators
    PLUS = auto()  # a + b
    INCR = auto() # ++a, a++
    MINUS = auto()  # a - b
    DECR = auto() # --a, a--
    MUL = auto()  # a * b
    DIV = auto()  # a / b
    MOD = auto()  # a % b

    # Comparison operators
    EQ = auto() # a == b
    NEQ = auto() # a != b
    LT = auto() # a < b
    LTE = auto() # a <= b
    GT = auto() # a > b
    GTE = auto() # a >= b

    # Logical Operators
    NOT = auto() # !a
    AND = auto() # a && b
    OR = auto() # a || b

    # Bitwise Operators
    BIT_NOT = auto() # ~a
    BIT_AND = auto() # a & b
    BIT_OR = auto() # a | b
    LSHIFT = auto() # a << b
    RSHIFT = auto() # a >> b

    # Compound Operators
    PLUS_EQ = auto() # a += b
    MINUS_EQ = auto() # a -= b
    MUL_EQ = auto() # a *= b
    DIV_EQ = auto() # a /= b
    MOD_EQ = auto() # a %= b
    BIT_AND_EQ = auto() # a &= b
    BIT_OR_EQ = auto() # a |= b
    LSHIFT_EQ = auto() # a <<= b
    RSHIFT_EQ = auto() # a >>= b

    # Member and Pointer Operators
    ARROW = auto() # a->b (member b of object pointed to by a)
    DOT = auto() # a.b (member b of object a)

    # Other Operators
    ASSIGNMENT = auto() #  a = b
    SEMICOLON = auto() # a;
    COMMA = auto() # a, b
    QUESTION = auto() # a ? b : c
    COLON = auto() # a ? b : c

    # Paired Symbols
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto() # [
    RBRACKET = auto() # ]
    
    # Comments
    LINE_COMMENT = auto() # //
    START_COMMENT = auto() # /*
    END_COMMENT = auto() # */

    # End of line and end of file
    EOLN = auto()  # new line
    EOF = auto()  # end of file

KEYWORDS = {
    "char": TK.CHAR,
    "short": TK.SHORT,
    "int": TK.INT,
    "signed": TK.SIGNED,
    "unsigned": TK.UNSIGNED,
    "long": TK.LONG,
    "float": TK.FLOAT,
    "double": TK.DOUBLE,
    "if": TK.IF,
    "else": TK.ELSE,
    "while": TK.WHILE,
    "do": TK.DO,
    "for": TK.FOR,
    "break": TK.BREAK,
    "continue": TK.CONTINUE,
    "void": TK.VOID
}

ARITH_OPERATORS = {
    "+": TK.PLUS,
    "-": TK.MINUS,
    "*": TK.MUL,
    "/": TK.DIV,
    "%": TK.MOD,
}

GLOBALS = {
    "CUR_TOKEN": None,
    "CUR_VALUE": "",

    "CUR_FILE": "",
    "CUR_LINE": 1,
    "CUR_COL": 0,
    "SCAN_P": 0,

    "MMAPPED_FILE": None
}
