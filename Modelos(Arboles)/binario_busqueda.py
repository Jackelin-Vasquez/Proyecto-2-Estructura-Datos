class Nodo:
    def __init__(self, val):
        self.val = val
        self.izq = None
        self.der = None
        self.altura = 0

class ArbolBusqueda:
    def __init__(self, nombre):
        self.raiz = None
        self.nombre = nombre
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


    def buscar(self, valor):
        if self.raiz:
            self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if nodo:
            if nodo.val == valor:
                return nodo.val, nodo.altura, nodo.prev
            self._buscar(nodo.izq, valor)
            self._buscar(nodo.der, valor)


    def eliminar(self, valor):
        if self.raiz:
            self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo:
            if valor < nodo.val:
                return self._eliminar(nodo.izq, valor)
            if valor > nodo.val:
                return self._eliminar(nodo.der, valor)

            if not nodo.der:
                return nodo.izq
            if not nodo.izq:
                return nodo.der

            sucesor = self.min(nodo.der)
            nodo.valor = sucesor.valor
            nodo.der = self._eliminar(nodo.der, sucesor.valor)

        return False

    def min(self, nodo):
        if nodo.izq:
            return self.min(nodo.izq)
        return nodo