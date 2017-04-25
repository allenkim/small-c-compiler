from setup import TK, TYPE

LABEL_NUM = 0

class BodyAST:
    """
    Statement sequences of nodes
    """
    def __init__(self):
        self.children = []

    def insert(self, node):
        self.children.append(node)

    def generate_assembly(self):
        assembly = ""
        for child in self.children:
            child_assembly = child.generate_assembly()
            if child_assembly:
                assembly += child_assembly
                assembly += "\n"
        return assembly

    def print(self):
        self.print_helper(0)

    def print_helper(self, level):
        pad = "  " * level
        print(pad + "BodyAST")
        for child in self.children:
            child.print_helper(level+1)

class ExprAST:
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

    def generate_assembly(self):
        if self.type == TYPE.DOUBLE:
            return "pushid {}".format(self.val)
        else:
            return "pushil {}".format(self.val)

class VariableExprAST(ExprAST):
    """
    Expression class for variables
    symbol: Symbol table element
    """
    def __init__(self, symbol, decl=False):
        self.symbol = symbol
        self.decl = decl

    def print_helper(self, level):
        pad = "  " * level
        symbol = self.symbol
        signed = symbol["signed"]
        flags = [flag.name for flag in symbol["flags"]]
        if signed == None:
            s = ""
        elif signed:
            s = "SIGNED"
        else:
            s = "UNSIGNED"
        declared = ""
        if self.decl:
            declared = "Declared "
        description = "{} {} {}".format(s, symbol["type"], symbol["name"])
        print(pad + "{}{} VariableExprAST: ".format(declared,flags) + description)

    def generate_assembly(self):
        if not self.decl:
            return "push {}".format(self.symbol["address"])


class UnaryExprAST(ExprAST):
    """
    Expression class for unary operator
    op: operator token
    operand: ExprAST
    """
    def __init__(self, op, operand, post=False):
        self.op = op
        self.operand = operand
        self.post = post

    def print_helper(self, level):
        pad = "  " * level
        typ = "PREFIX"
        if self.post:
            typ = "POSTFIX"
        print(pad + "{} UnaryExpr: {}".format(typ, self.op))
        self.operand.print_helper(level+1)

    def generate_assembly(self):
        operand_code = self.operand.generate_assembly()
        commands = [operand_code]
        if self.op == TK.NOT:
            commands.append("not")
            return "\n".join(commands)
        elif self.op == TK.BIT_NOT:
            commands.append("bitnot")
            return "\n".join(commands)
        elif self.op == TK.INCR:
            addr = self.operand.symbol["address"]
            if self.post:
                commands.append("push {}".format(addr))
                commands.append("incr {}".format(addr))
            else:
                commands.append("incr {}".format(addr))
                commands.append("push {}".format(addr))
            return "\n".join(commands)
        elif self.op == TK.DECR:
            addr = self.operand.symbol["address"]
            if self.post:
                commands.append("push {}".format(addr))
                commands.append("decr {}".format(addr))
            else:
                commands.append("decr {}".format(addr))
                commands.append("push {}".format(addr))
            return "\n".join(commands)


class BinaryExprAST(ExprAST):
    """
    Expression class for binary operator
    op: operator token
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

    def generate_assembly(self):
        l = self.lhs.generate_assembly()
        r = self.rhs.generate_assembly()
        commands = [l,r]
        if self.op == TK.PLUS:
            commands.append("add")
            return "\n".join(commands)
        elif self.op == TK.MINUS:
            commands.append("sub")
            return "\n".join(commands)
        elif self.op == TK.MUL:
            commands.append("mul")
            return "\n".join(commands)
        elif self.op == TK.DIV:
            commands.append("div")
            return "\n".join(commands)
        elif self.op == TK.MOD:
            commands.append("mod")
            return "\n".join(commands)
        elif self.op == TK.EQ:
            commands.append("eq")
            return "\n".join(commands)
        elif self.op == TK.NEQ:
            commands.append("neq")
            return "\n".join(commands)
        elif self.op == TK.LT:
            commands.append("lt")
            return "\n".join(commands)
        elif self.op == TK.LTE:
            commands.append("lte")
            return "\n".join(commands)
        elif self.op == TK.GT:
            commands.append("gt")
            return "\n".join(commands)
        elif self.op == TK.GTE:
            commands.append("gte")
            return "\n".join(commands)
        elif self.op == TK.AND:
            commands.append("and")
            return "\n".join(commands)
        elif self.op == TK.OR:
            commands.append("or")
            return "\n".join(commands)
        elif self.op == TK.BIT_AND:
            commands.append("bitand")
            return "\n".join(commands)
        elif self.op == TK.BIT_OR:
            commands.append("bitor")
            return "\n".join(commands)
        elif self.op == TK.BIT_XOR:
            commands.append("xor")
            return "\n".join(commands)
        elif self.op == TK.LSHIFT:
            commands.append("shl")
            return "\n".join(commands)
        elif self.op == TK.RSHIFT:
            commands.append("shr")
            return "\n".join(commands)
        elif self.op == TK.PLUS_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("add")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.MINUS_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("sub")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.MUL_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("mul")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.DIV_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("div")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.MOD_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("mod")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.BIT_AND_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("bitand")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.BIT_OR_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("bitor")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.BIT_XOR_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("xor")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.LSHIFT_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("shl")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.RSHIFT_EQ:
            commands = []
            commands.append("push {}".format(self.lhs.symbol["address"]))
            commands.append(r)
            commands.append("shr")
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        elif self.op == TK.ASSIGNMENT:
            commands = [r]
            commands.append("pop {}".format(self.lhs.symbol["address"]))
            return '\n'.join(commands)
        else:
            raise ValueError("Unknown op in parse tree")
            

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

    def generate_assembly(self):
        return ""

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

    def generate_assembly(self):
        return ""

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

    def generate_assembly(self):
        if self.proto.symbol["name"] == "main":
            return self.body.generate_assembly()
        else:
            return ""

class ReturnAST:
    """
    Return statement in a function
    """
    def __init__(self, expr):
        self.expr = expr

    def print_helper(self, level):
        pad = "  " * level
        print(pad + "ReturnAST")
        self.expr.print_helper(level+1)

    def generate_assembly(self):
        return "halt"

class IfAST:
    """
    Expression for if statements
    """
    def __init__(self, cond, body, els):
        self.cond = cond
        self.body = body
        self.els = els

    def print_helper(self, level):
        pad = "  " * level
        print(pad + "IfExpr:")
        self.cond.print_helper(level+1)
        self.body.print_helper(level+1)
        self.els.print_helper(level+1)

    def generate_assembly(self):
        global LABEL_NUM
        label_num = LABEL_NUM
        LABEL_NUM += 2
        commands = []
        commands.append(self.cond.generate_assembly())
        commands.append("jfalse L{}".format(label_num))
        commands.append(self.body.generate_assembly())
        commands.append("jmp L{}".format(label_num+1))
        commands.append("L{}:".format(label_num))
        els = ""
        if self.els:
            els = self.els.generate_assembly()
            commands.append(els)
            commands.append("L{}:".format(label_num+1))
        else:
            commands.pop(3)
        return "\n".join(commands)

class DoWhileAST:
    """
    Expression for Do-While statements
    """
    def __init__(self, body, cond):
        self.body = body
        self.cond = cond

    def print_helper(self, level):
        pad = "  " * level
        print(pad + "DoWhileExpr:")
        self.body.print_helper(level+1)
        self.cond.print_helper(level+1)

    def generate_assembly(self):
        global LABEL_NUM
        label_num = LABEL_NUM
        LABEL_NUM += 1
        commands = []
        commands.append("L{}:".format(label_num))
        commands.append(self.body.generate_assembly())
        commands.append(self.cond.generate_assembly())
        commands.append("jtrue L{}".format(label_num))
        return "\n".join(commands)

