from Arboles.base import ArbolPorNiveles, NodoBase
from Recorridos import recorridos


class Nodo(NodoBase):
    pass


class ArbolBusqueda(ArbolPorNiveles):
    def agregar(self, val):
        if self.raiz is None:
            self.raiz = Nodo(val)
            self.altura_max = 1
            return True
        return self._agregar(self.raiz, val, 2)

    def _agregar(self, root, val, nivel):
        if val == root.val:
            print("No se puede agregar: valor duplicado")
            return False

        if val < root.val:
            if root.izq is None:
                root.izq = Nodo(val)
                root.izq.altura = nivel
                self.altura_max = max(self.altura_max, nivel)
                return True
            return self._agregar(root.izq, val, nivel + 1)

        if root.der is None:
            root.der = Nodo(val)
            root.der.altura = nivel
            self.altura_max = max(self.altura_max, nivel)
            return True
        return self._agregar(root.der, val, nivel + 1)

    def buscar(self, valor):
        encontrado = recorridos.nodo_ordenado(self.raiz, valor)
        if encontrado is None:
            return None
        nodo, _ = encontrado
        return nodo.val, nodo.altura

    def eliminar(self, valor):
        self.raiz = recorridos.eliminar_ordenado(self.raiz, valor)
        self._actualizar_niveles()
