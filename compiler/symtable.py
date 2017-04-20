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

class SingleTable:
    """
    Single symbol table (represents one scope)
    """
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent
        self.children = []

    def lookup(self, name):
        if name in self.table:
            return self.table[name]
        return None

    def insert(self, symb):
        name = symb["name"]
        if self.lookup(name):
            processing_error("'{}' already initialized".format(name))
        symb["table"] = self
        self.table[name] = symb
        return symb

class SymbolTable:
    """
    Stack of symbol tables (keeps track of scope)
    """
    def __init__(self):
        self.current = SingleTable()
        self.address = 0

    def enter_scope(self):
        new_table = SingleTable(self.current)
        self.current.children.append(new_table)
        self.current = new_table

    def exit_scope(self):
        self.current = self.current.parent

    def local_lookup(self, name):
        sym = self.current.lookup()
        if sym:
            return sym
        return None

    def lookup(self, name):
        check = self.current
        while check != None:
            sym = check.lookup(name)
            if check.lookup:
                return sym
            check = check.parent
        return None

    def insert_symbol(self, symb):
        typ = symb["type"]
        if symb["id_type"] == TK.VAR:
            symb["address"] = self.address
            self.address += TYPE_SIZE[typ]
        self.current.insert(symb)
        return symb

    def insert(self, name, id_typ, flags, typ, signed=None):
        new_symbol = make_symbol(name, id_typ, flags, typ, signed)
        self.insert_symbol(new_symbol)
        return new_symbol

