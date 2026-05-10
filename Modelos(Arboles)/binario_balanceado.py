class Nodo:
    def __init__(self, val):
        self.val = val
        self.izq = None
        self.der = None
        self.altura = 0

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def altura(self, nodo):
        if nodo is None:
            return -1
        return nodo.altura

    def agregar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        self._agregar(valor, self.raiz)

    def _agregar(self, valor, nodo):
        if valor == nodo.val:
            return False
        if valor < nodo.val:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
                return True
            return self._agregar(valor, nodo.izq)

        if nodo.der is None:
            nodo.der = Nodo(valor)
            return True
        return self._agregar(valor, nodo.der)

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)

        if valor < nodo.val:
            nodo.izq = self._insertar(nodo.izq, valor)
        elif valor > nodo.val:
            nodo.der = self._insertar(nodo.der, valor)
        nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))
        return Nodo

    def balance(self):
        bal = self.altura(self.izq) - self.altura(self.der)
        if bal > 1:
            print("desbalance hacia la derecha")
            return "der"
        if bal < -1:
            print("Desbalance hacia la izquierda")
            return "izq"
        return True

    def rebal(self):
        if self.balance() == "der":
            if self.izq.balance() == "izq":
                print("Rotacion simple a la derecha")
                return self.rotacion_der()

            print("Rotacion doble a la derecha")
            self.izq.rotacion_izq()
            return self.rotacion_der()
        if self.balance() == "izq":
            if self.der.balance() == "der":
                print("Rotacion simple a la izquierda")
                return self.rotacion_izq()

            print("Rotacion doble a la izquierda")
            self.der.rotacion_der()
            return self.rotacion_izq()

    def rotacion_der(self):
        new_root = self.izq
        self.izq = new_root.der
        new_root.der = self
        self.altura = 1 + max(self.altura(self.izq), self.altura(self.der))
        new_root.altura = 1 + max(self.altura(new_root.izq), self.altura(new_root.der))
        return new_root

    def rotacion_izq(self):
        new_root = self.der
        self.der = new_root.izq
        new_root.izq = self
        self.altura = 1 + max(self.altura(self.izq), self.altura(self.der))
        new_root.altura = 1 + max(self.altura(new_root.izq), self.altura(new_root.der))
        return new_root

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