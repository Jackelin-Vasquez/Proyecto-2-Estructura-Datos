from Arboles.base import ArbolPorNiveles, NodoBase
from Recorridos import recorridos


class Nodo(NodoBase):
    def __init__(self, val):
        super().__init__(val, altura=0)
        self.prev = None


class ArbolSimple(ArbolPorNiveles):
    asignar_prev = True

    def agregar(self, val):
        nodo = Nodo(val)
        if not self.raiz:
            nodo.altura = 1
            self.raiz = nodo
            self.altura_max = 1
            return True
        return self._agregar(nodo, [self.raiz], 2)

    def _agregar(self, nodo, fila, h):
        cant = len(fila)
        while cant > 0:
            c_node = fila.pop(0)
            cant -= 1
            if nodo.val == c_node.val:
                return False
            if not c_node.izq:
                nodo.altura = h
                nodo.prev = c_node.val
                c_node.izq = nodo
                self.altura_max = max(self.altura_max, h)
                return True
            if not c_node.der:
                nodo.altura = h
                nodo.prev = c_node.val
                c_node.der = nodo
                self.altura_max = max(self.altura_max, h)
                return True
            fila.append(c_node.izq)
            fila.append(c_node.der)
        return self._agregar(nodo, fila, h + 1)

    def buscar(self, valor):
        if self.raiz:
            return self._buscar(self.raiz, valor)
        return None

    def _buscar(self, nodo, valor):
        if nodo is None:
            return None
        if nodo.val == valor:
            return nodo.val, nodo.altura, nodo.prev

        encontrado = self._buscar(nodo.izq, valor)
        if encontrado:
            return encontrado
        return self._buscar(nodo.der, valor)

    def eliminar(self, valor):
        if self.raiz is None:
            return False
        eliminado = self._eliminar(self.raiz, None, valor)
        if eliminado:
            self._actualizar_niveles()
        return eliminado

    def _eliminar(self, nodo, padre, valor):
        if nodo is None:
            return False

        if nodo.val == valor:
            self._eliminar_nodo(nodo, padre)
            return True

        return self._eliminar(nodo.izq, nodo, valor) or self._eliminar(nodo.der, nodo, valor)

    def _eliminar_nodo(self, nodo, padre):
        valores = []
        recorridos.recolectar_valores(nodo.izq, valores)
        recorridos.recolectar_valores(nodo.der, valores)

        if padre is None:
            self.raiz = None
        elif padre.izq == nodo:
            padre.izq = None
        elif padre.der == nodo:
            padre.der = None

        for valor in valores:
            self.agregar(valor)
