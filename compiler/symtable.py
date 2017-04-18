from setup import TK, TYPE_SIZE
from error_handling import processing_error

class SymbolTable:
    """
    Stack of symbol tables (keeps track of scope)
    """
    def __init__(self):
        self.stack = [{}]
        self.address = [0]

    def start_new_scope(self):
        self.stack.append({})
        self.address.append(0)

    def close_scope(self):
        self.stack.pop()
        return self.address.pop()

    def lookup(self, name):
        last_idx = len(self.stack) - 1
        while last_idx >= 0:
            if name in self.stack[last_idx]:
                return self.stack[last_idx][name]
            last_idx -= 1
        return None

    def insert(self, name, id_typ, flags, typ, signed=True):
        """
        name: string of id name
        id_typ: token of identifier (variable, function, ..._
        flags: array of flag tokens (ex. TK.CONST, TK.STATIC, ...)
        typ: type token
        signed: (optional) True or False
        """
        if name in self.stack[-1]:
            processing_error("{} already initialized".format(id_name))
        new_symbol = {
            "name": name,
            "id_type": id_typ,
            "flags": flags,
            "type": typ,
            "signed": signed,
        }
        if id_typ == TK.VAR:
            new_symbol["address"] = self.address[-1]
            self.address[-1] += TYPE_SIZE[typ]
        self.stack[-1][name] = new_symbol
