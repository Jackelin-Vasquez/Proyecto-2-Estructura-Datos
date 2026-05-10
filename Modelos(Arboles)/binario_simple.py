class Nodo:
    def __init__(self, val):
        self.val = val
        self.izq = None
        self.der = None
        self.altura = 0


class ArbolSimple:
    def __init__(self, raiz):
        self.raiz = raiz
        self.altura_max = 0

    def agregar(self, val):
        nodo = Nodo(val)
        fila = []
        if not self.raiz:
            nodo.altura = 1
            self.raiz = nodo
            return
        self._agregar(nodo, fila, 2)

    def _agregar(self, nodo, fila, h):
        cant = len(fila)
        while cant > 0:
            c_node = fila.pop(0)
            if not c_node.izq:
                nodo.altura = h
                c_node.izq = nodo
                self.altura_max = h
                return
            if not c_node.der:
                nodo.altura = h
                c_node.der = nodo
                self.altura_max = h
                return
            fila.append(c_node.izq)
            fila.append(c_node.der)
        return self._agregar(nodo, fila, h + 1)

    def preorden(self):
        if self.raiz:
            self._preorden(self.raiz)

    def _preorden(self, nodo):
        print(nodo.val)
        self._preorden(nodo.izq)
        self._preorden(nodo.der)

    def inorden(self):
        if self.raiz:
            self._inorden(self.raiz)

    def _inorden(self, nodo):
        self._inorden(nodo.izq)
        print(nodo.val)
        self._inorden(nodo.der)

    def postorden(self):
        if self.raiz:
            self._postorden(self.raiz)

    def _postorden(self, nodo):
        self._postorden(nodo.izq)
        self._postorden(nodo.der)
        print(nodo.val)

    def buscar(self): pass
    def eliminar(self): pass
    def altura(self): pass