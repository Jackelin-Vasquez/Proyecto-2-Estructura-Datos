class Nodo:
    def __init__(self, val):
        self.val = val
        self.izq = None
        self.der = None
        self.altura = 0

class ArbolBusqueda:
    def __init__(self):
        self.raiz = None
        self.altura_max = 0


    def agregar(self, val):
        nodo = Nodo(val)
        if self.raiz:
            self._agregar(self.raiz, nodo)
            return
        self.raiz = nodo

    def _agregar(self, root, nodo):
        if nodo.val == root.val:
            print("No se puede agregar: valor duplicado")
            return False
        if nodo.val < root.val:
            if root.izq:
                self._agregar(root.izq, nodo)
            root.izq = nodo
            return

        if nodo.val > root.val:
            if root.der:
                self._agregar(root.der, nodo)
            root.der = nodo
            return


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

