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

class VariableExprAST(ExprAST):
    """
    Expression class for variables
    name: name of the variable
    """
    def __init__(self, name, typ, signed):
        super().__init__(typ, signed)
        self.name = name

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

class CallExprAST(ExprAST):
    """
    Expression class for function calls
    callee: string of function
    args: array of ExprAST
    """
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

class PrototypeAST:
    """
    Prototype of a function, name and arguments
    return_type: char, short, int, long, float, double
    name: string
    args: vector of strings
    """
    def __init__(self, name, args, typ, signed):
        super().__init__(typ, signed)
        self.name = name
        self.args = args

class FunctionAST:
    """
    Function definition itself
    proto: PrototypeAST
    body: ExprAST
    """
    def __init__(self, proto, body):
        self.proto = proto
        self.body = body

