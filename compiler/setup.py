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
    FLOATLIT = auto() # 1.2f, 3.5F 
    DOUBLELIT = auto() # 0.0, 1.2, 3.0 / 2, ... 
    STRINGLIT = auto()  # "hello", "world", ...
    ID = auto()  # a, abc, ab123, ...

    # Types of Identifiers
    VAR = auto() # standard variables
    POINTER = auto() # pointers
    FUNC = auto() # functions

    # Primitive types
    SIGNED = auto()  # either prefix or interpreted as int
    UNSIGNED = auto()  # either prefix or interpreted as unsigned int
    CHAR = auto()  # 1 byte (unsigned)
    SHORT = auto()  # either prefix (short int) or 2 bytes (signed short)
    INT = auto()  # 4 bytes (signed)
    LONG = auto()  # either prefix (long long, ...)  or 8 bytes (signed long)
    FLOAT = auto()  # 4 bytes
    DOUBLE = auto()  # 8 bytes

    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    DO = auto()
    FOR = auto()
    BREAK = auto()
    CONTINUE = auto()
    SIZEOF = auto()
    STRUCT = auto()
    VOID = auto()
    RETURN = auto()
    SWITCH = auto()
    CASE = auto()
    DEFAULT = auto()
    CONST = auto()
    STATIC = auto()
    TYPEDEF = auto()
    ENUM = auto()
    GOTO = auto()
    UNION = auto()
    AUTO = auto()
    REGISTER = auto()
    VOLATILE = auto()
    EXTERN = auto()

    # Arithmetic Operators
    PLUS = auto()  # a + b
    INCR = auto()  # ++a, a++
    MINUS = auto()  # a - b
    DECR = auto()  # --a, a--
    MUL = auto()  # a * b
    DIV = auto()  # a / b
    MOD = auto()  # a % b

    # Comparison operators
    EQ = auto()  # a == b
    NEQ = auto()  # a != b
    LT = auto()  # a < b
    LTE = auto()  # a <= b
    GT = auto()  # a > b
    GTE = auto()  # a >= b

    # Logical Operators
    NOT = auto()  # !a
    AND = auto()  # a && b
    OR = auto()  # a || b

    # Bitwise Operators
    BIT_NOT = auto()  # ~a
    BIT_AND = auto()  # a & b
    BIT_OR = auto()  # a | b
    BIT_XOR = auto() # a ^ b
    LSHIFT = auto()  # a << b
    RSHIFT = auto()  # a >> b

    # Compound Operators
    PLUS_EQ = auto()  # a += b
    MINUS_EQ = auto()  # a -= b
    MUL_EQ = auto()  # a *= b
    DIV_EQ = auto()  # a /= b
    MOD_EQ = auto()  # a %= b
    BIT_AND_EQ = auto()  # a &= b
    BIT_OR_EQ = auto()  # a |= b
    BIT_XOR_EQ = auto() # a ^= b
    LSHIFT_EQ = auto()  # a <<= b
    RSHIFT_EQ = auto()  # a >>= b

    # Member and Pointer Operators
    ARROW = auto()  # a->b (member b of object pointed to by a)
    DOT = auto()  # a.b (member b of object a)

    # Other Operators
    ASSIGNMENT = auto()  # a = b
    SEMICOLON = auto()  # a;
    COMMA = auto()  # a, b
    
    QUESTION = auto() # a ? b : c
    COLON = auto()  # a ? b : c

    # Paired Symbols
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]

    # End of file
    EOF = auto()  # end of file

class TYPE(Enum):
    #SIGNED_CHAR = auto() # signed char, 1 byte
    #UNSIGNED_CHAR = auto() # char, unsigned char
    CHAR = auto()
    #SIGNED_SHORT = auto() # short, short int, signed short, signed short int, 2 bytes
    #UNSIGNED_SHORT = auto() # unsigned short, unsigned short int
    SHORT = auto()
    #SIGNED_INT = auto() # int, signed, signed int, 4 bytes
    #UNSIGNED_INT = auto() # unsigned, unsigned int
    INT = auto()
    #SIGNED_LONG = auto() # long, long int, signed long, signed long int, 8 bytes
    #UNSIGNED_LONG = auto() # unsigned long, unsigned long int
    #SIGNED_LONG_LONG = auto() # long long, signed long long, signed long long int, 8 bytes
    #UNSIGNED_LONG_LONG = auto() # unsigned long long, unsigned long long int
    LONG = auto()

    FLOAT = auto() # float, 4 bytes
    DOUBLE = auto() # double, long double 8 bytes

    VOID = auto() # void for use in functions

TYPE_SIZE = {
    TYPE.CHAR: 1,
    TYPE.SHORT: 2,
    TYPE.INT: 4,
    TYPE.LONG: 8,
    TYPE.FLOAT: 4,
    TYPE.DOUBLE: 8,
}

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
    "sizeof": TK.SIZEOF,
    "struct": TK.STRUCT,
    "void": TK.VOID,
    "return": TK.RETURN,
    "switch": TK.SWITCH,
    "case": TK.CASE,
    "default": TK.DEFAULT,
    "const": TK.CONST,
    "static": TK.STATIC,
    "typedef": TK.TYPEDEF,
    "enum": TK.ENUM,
    "goto": TK.GOTO,
    "union": TK.UNION,
    "auto": TK.AUTO, 
    "register": TK.REGISTER,
    "volatile": TK.VOLATILE,
    "extern": TK.EXTERN,
}

OPERATORS = {
    "L1": {
        "+": TK.PLUS,
        "-": TK.MINUS,
        "*": TK.MUL,
        "/": TK.DIV,
        "%": TK.MOD,
        "<": TK.LT,
        ">": TK.GT,
        "!": TK.NOT,
        "~": TK.BIT_NOT,
        "&": TK.BIT_AND,
        "|": TK.BIT_OR,
        "^": TK.BIT_XOR,
        ".": TK.DOT,
        "=": TK.ASSIGNMENT,
        ";": TK.SEMICOLON,
        ",": TK.COMMA,
        "?": TK.QUESTION,
        ":": TK.COLON,
        "(": TK.LPAREN,
        ")": TK.RPAREN,
        "{": TK.LBRACE,
        "}": TK.RBRACE,
        "[": TK.LBRACKET,
        "]": TK.RBRACKET,
    },
    "L2": {
        "+=": TK.PLUS_EQ,
        "++": TK.INCR,
        "-=": TK.MINUS_EQ,
        "--": TK.DECR,
        "&&": TK.AND,
        "||": TK.OR,
        "*=": TK.MUL_EQ,
        "/=": TK.DIV_EQ,
        "%=": TK.MOD_EQ,
        "<=": TK.LTE,
        ">=": TK.GTE,
        "!=": TK.NEQ,
        "&=": TK.BIT_AND_EQ,
        "|=": TK.BIT_OR_EQ,
        "^=": TK.BIT_XOR_EQ,
        "<<": TK.LSHIFT,
        ">>": TK.RSHIFT,
        "->": TK.ARROW,
        "==": TK.EQ,
    },
    "L3": {
        "<<=": TK.LSHIFT_EQ,
        ">>=": TK.RSHIFT_EQ,
    }
}

class OP(Enum):
    """
    Enumeration of all supported op codes
    """
    # Data Movement
    PUSH = 0
    PUSHIL = 23
    PUSHID = 24
    POP = 1
    
    # Arithmetic
    ADD = 2
    SUB = 3
    MUL = 4
    DIV = 5
    MOD = 6

    INCR = 28
    DECR = 29

    # Comparison
    EQ = 7
    NEQ = 8
    LT = 9
    LTE = 10
    GT = 11
    GTE = 12

    # Logic
    NOT = 25
    AND = 26
    OR = 27

     # Bitwise
    BIT_NOT = 13
    BIT_AND = 14
    BIT_OR = 15
    XOR = 16
    LSHIFT = 17
    RSHIFT = 18

    # Jumps
    JMP = 19
    JFALSE = 20
    JTRUE = 21

    HALT = 30
    NOP = 31


GLOBALS = {
    "CUR_TOKEN": None,
    "CUR_VALUE": "",

    "CUR_FILE": "",
    "CUR_LINE": 1,
    "CUR_COL": 0,
    "SCAN_P": 0,

    "MMAPPED_FILE": None,
    "BINOP_PRECEDENCE": {},
    "SYMBOL_TABLE": {},
}
