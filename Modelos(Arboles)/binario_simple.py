class Nodo:
    def __init__(self, val):
        self.val = val
        self.izq = None
        self.prev = None
        self.der = None
        self.altura = 0


class ArbolSimple:
    def __init__(self, nombre):
        self.raiz = None
        self.nombre = nombre
        self.altura_max = 0

    def agregar(self, val):
        nodo = Nodo(val)
        fila = []
        if not self.raiz:
            nodo.altura = 1
            self.raiz = nodo
            return
        fila.append(self.raiz)
        self._agregar(nodo, fila, 2)

    def _agregar(self, nodo, fila, h):
        cant = len(fila)
        while cant > 0:
            c_node = fila.pop(0)
            if nodo.val == c_node.val:
                return False
            if not c_node.izq:
                nodo.altura = h
                nodo.prev = c_node.val
                c_node.izq = nodo
                self.altura_max = h if h > nodo.altura else nodo.altura
                return
            if not c_node.der:
                nodo.altura = h
                nodo.prev = c_node.val
                c_node.der = nodo
                self.altura_max = h if h > nodo.altura else nodo.altura
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


    def buscar(self, valor):
        if self.raiz:
            self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if nodo:
            if nodo.val == valor:
                return nodo.val, nodo.altura, nodo.prev
            self._buscar(nodo.izq, valor)
            self._buscar(nodo.der, valor)


    def eliminar(self, nodo, valor):
        if nodo:
            if nodo.val == valor:
                self._eliminar(nodo)
                return
            self.eliminar(nodo.izq, valor)
            self.eliminar(nodo.der, valor)


    def _eliminar(self, nodo):
        dizq_val, nod_izq, d_izq = self.p_izq(nodo)
        dder_val, nod_der, d_der = self.p_der(nodo)
        if d_izq == d_der or d_izq < d_der:
            if nod_izq:
                nodo.val = dizq_val
                nod_izq.izq = None
                return
            nodo.val = nodo.izq.val
            nodo.izq = None
            return

        if d_izq > d_der:
            if nod_der:
                nodo.val = dder_val
                nod_der.der = None
                nod_der.izq = None
                return
            nodo.val = nodo.der.val
            nodo.der = None
            return

    def p_izq(self, nodo, d = 0):
        if nodo.izq.izq:
            return self.p_izq(nodo.izq, d + 1)
        return nodo.izq.val if nodo.izq else nodo, nodo if nodo.izq else None, d
    def p_der(self, nodo, d = 0):
        if nodo.der.der:
            return self.p_der(nodo.der, d + 1)
        return nodo.der.val if nodo.der else nodo, nodo if nodo.der else None, d