from setup import TK, TYPE_SIZE
from error_handling import processing_error

def make_symbol(name, id_typ, flags, typ, signed=True):
    """
    name: string of id name
    id_typ: token of identifier (variable, function, ..._
    flags: array of flag tokens (ex. TK.CONST, TK.STATIC, ...)
    typ: type token
    signed: (optional) True or False
    address: location in memory (specified only if existing already)
    """
    new_symbol = {
        "name": name,
        "id_type": id_typ,
        "flags": flags,
        "type": typ,
        "signed": signed,
    }
    return new_symbol

class SymbolTable:
    """
    Stack of symbol tables (keeps track of scope)
    """
    def __init__(self):
        self.stack = [{}]
        self.address = 0

    def enter_scope(self):
        self.stack.append({})

    def exit_scope(self):
        self.stack.pop()

    def local_lookup(self, name):
        if name in self.stack[-1]:
            return self.stack[-1][name]
        return None

    def lookup(self, name):
        last_idx = len(self.stack) - 1
        while last_idx >= 0:
            if name in self.stack[last_idx]:
                return self.stack[last_idx][name]
            last_idx -= 1
        return None

    def insert_symbol(self, symb):
        name = symb["name"]
        typ = symb["type"]
        if self.local_lookup(name):
            processing_error("'{}' already initialized".format(name))
        if symb["id_type"] == TK.VAR:
            symb["address"] = self.address
            self.address += TYPE_SIZE[typ]
        self.stack[-1][name] = symb
        return symb

    def insert(self, name, id_typ, flags, typ, signed=True):
        new_symbol = make_symbol(name, id_typ, flags, typ, signed)
        self.insert_symbol(new_symbol)
        return new_symbol
