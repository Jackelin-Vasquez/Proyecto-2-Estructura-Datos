from Arboles.base import ArbolBase, NodoBase
from Recorridos import recorridos


class Nodo(NodoBase):
    pass


class ArbolAVL(ArbolBase):
    def altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def agregar(self, valor):
        return self.insertar(valor)

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)
        return True

    def _insertar(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)

        if valor < nodo.val:
            nodo.izq = self._insertar(nodo.izq, valor)
        elif valor > nodo.val:
            nodo.der = self._insertar(nodo.der, valor)
        else:
            print("No se puede agregar: valor duplicado")
            return nodo

        self._actualizar_altura(nodo)
        balance = self.balance(nodo)

        if balance > 1:
            if valor < nodo.izq.val:
                return self.rotacion_der(nodo)
            nodo.izq = self.rotacion_izq(nodo.izq)
            return self.rotacion_der(nodo)

        if balance < -1:
            if valor > nodo.der.val:
                return self.rotacion_izq(nodo)
            nodo.der = self.rotacion_der(nodo.der)
            return self.rotacion_izq(nodo)

        return nodo

    def balance(self, nodo):
        if nodo is None:
            return 0
        return self.altura(nodo.izq) - self.altura(nodo.der)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))

    def rotacion_der(self, nodo):
        new_root = nodo.izq
        temp = new_root.der

        new_root.der = nodo
        nodo.izq = temp

        self._actualizar_altura(nodo)
        self._actualizar_altura(new_root)
        return new_root

    def rotacion_izq(self, nodo):
        new_root = nodo.der
        temp = new_root.izq

        new_root.izq = nodo
        nodo.der = temp

        self._actualizar_altura(nodo)
        self._actualizar_altura(new_root)
        return new_root

    def buscar(self, valor):
        return recorridos.buscar_ordenado(self.raiz, valor)

    def eliminar(self, valor):
        self.raiz = recorridos.eliminar_ordenado(self.raiz, valor, self._reequilibrar)

    def _reequilibrar(self, nodo):
        self._actualizar_altura(nodo)
        balance = self.balance(nodo)

        if balance > 1:
            if self.balance(nodo.izq) >= 0:
                return self.rotacion_der(nodo)
            nodo.izq = self.rotacion_izq(nodo.izq)
            return self.rotacion_der(nodo)

        if balance < -1:
            if self.balance(nodo.der) <= 0:
                return self.rotacion_izq(nodo)
            nodo.der = self.rotacion_der(nodo.der)
            return self.rotacion_izq(nodo)

        return nodo

    def recalcular_metadata(self):
        recorridos.recalcular_alturas(self.raiz)
