class BodyAST:
    """
    Statement sequences of nodes
    """
    def __init__(self):
        self.children = []

    def insert(self, node):
        self.children.append(node)

    def print(self):
        self.print_helper(0)

    def print_helper(self, level):
        pad = "  " * level
        print(pad + "BodyAST")
        for child in self.children:
            child.print_helper(level+1)

class ExprAST():
    """
    Base class for all expression nodes
    typ: char, short, int, long, float, double
    signed: True, False (whether it is signed)
    """
    def __init__(self, typ, signed):
        self.type = typ
        self.signed = signed

class NumberExprAST(ExprAST):
    """
    Expression class for all numeric literals
    val: 1.0, 3e-2, 4, etc...
    """
    def __init__(self, val, typ, signed):
        super().__init__(typ, signed)
        self.val = val

    def print_helper(self, level):
        pad = "  " * level
        if self.signed == None:
            s = ""
        elif self.signed:
            s = "SIGNED"
        else:
            s = "UNSIGNED"
        description = "{} {} - val: {}".format(s, self.type, self.val)
        print(pad + "NumberExprAST: " + description)

class VariableExprAST(ExprAST):
    """
    Expression class for variables
    symbol: Symbol table element
    """
    def __init__(self, symbol):
        self.symbol = symbol

    def print_helper(self, level):
        pad = "  " * level
        symbol = self.symbol
        signed = symbol["signed"]
        if signed == None:
            s = ""
        elif signed:
            s = "SIGNED"
        else:
            s = "UNSIGNED"
        description = "{} {} {}".format(s, symbol["type"], symbol["name"])
        print(pad + "VariableExprAST: " + description)


class BinaryExprAST(ExprAST):
    """
    Expression class for binary operator
    op: operator string
    lhs: ExprAST on the left hand side
    rhs: ExprAST on the right hand side
    """
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def print_helper(self, level):
        pad = "  " * level
        print(pad + "BinaryExprAST: {}".format(self.op))
        self.lhs.print_helper(level+1)
        self.rhs.print_helper(level+1)


class CallExprAST(ExprAST):
    """
    Expression class for function calls
    callee: string of function
    args: array of ExprAST
    """
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args
        
    def print_helper(self, level):
        pad = "  " * level
        print(pad + "CallExprAST: " + self.callee)
        for arg in self.args:
            arg.print_helper(level+1)

class PrototypeAST:
    """
    Prototype of a function, name and arguments
    fn_symbol: symbol table element for the function
    args: vector of symbol table elements
    """
    def __init__(self, fn_symbol, args):
        self.symbol = fn_symbol
        self.args = args

    def print_helper(self, level):
        pad = "  " * level
        symbol = self.symbol
        signed = symbol["signed"]
        if signed == None:
            s = ""
        elif signed:
            s = "SIGNED"
        else:
            s = "UNSIGNED"
        description = "{} {} {}".format(s, symbol["type"], symbol["name"])
        print(pad + "PrototypeAST: " + description)


class FunctionAST:
    """
    Function definition itself
    proto: PrototypeAST
    body: ExprAST
    """
    def __init__(self, proto, body):
        self.proto = proto
        self.body = body

    def print_helper(self, level):
        pad = "  " * level
        print(pad + "FunctionAST")
        self.proto.print_helper(level+1)
        self.body.print_helper(level+1)


