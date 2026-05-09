class Nodo:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.izq = None
        self.der = None
        self.altura = 0


class ArbolSimple:
    def __init__(self, raiz):
        self.raiz = raiz
        self.altura = 0

    def agregar(self): pass
    def buscar(self): pass
    def eliminar(self): pass
    def altura(self): pass