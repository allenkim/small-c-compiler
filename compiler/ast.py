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
        pad = '\t' * level
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
        pad = '\t' * level
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
    name: name of the variable
    """
    def __init__(self, name, typ, signed):
        super().__init__(typ, signed)
        self.name = name

    def print_helper(self, level):
        pad = '\t' * level
        if self.signed == None:
            s = ""
        elif self.signed:
            s = "SIGNED"
        else:
            s = "UNSIGNED"
        description = "{} {} {}".format(s, self.type, self.name)
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
        pad = '\t' * level
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

class PrototypeAST:
    """
    Prototype of a function, name and arguments
    return_type: char, short, int, long, float, double
    signed: True or False for the return type
    name: string
    args: vector of strings
    """
    def __init__(self, return_type, signed, name, args):
        self.return_type = return_type
        self.signed = signed
        self.name = name
        self.args = args

    def print_helper(self, level):
        pad = '\t' * level
        if self.signed == None:
            s = ""
        elif self.signed:
            s = "SIGNED"
        else:
            s = "UNSIGNED"
        description = "{} {} {}()".format(s, self.return_type, self.name)
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
        pad = '\t' * level
        print(pad + "FunctionAST")
        self.proto.print_helper(level+1)
        self.body.print_helper(level+1)


