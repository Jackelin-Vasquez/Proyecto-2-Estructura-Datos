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
            self.altura_max = 1
            return True
        fila.append(self.raiz)
        return self._agregar(nodo, fila, 2)

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

    def preorden(self):
        if self.raiz:
            self._preorden(self.raiz)

    def _preorden(self, nodo):
        if nodo is None:
            return
        print(nodo.val)
        self._preorden(nodo.izq)
        self._preorden(nodo.der)

    def inorden(self):
        if self.raiz:
            self._inorden(self.raiz)

    def _inorden(self, nodo):
        if nodo is None:
            return
        self._inorden(nodo.izq)
        print(nodo.val)
        self._inorden(nodo.der)

    def postorden(self):
        if self.raiz:
            self._postorden(self.raiz)

    def _postorden(self, nodo):
        if nodo is None:
            return
        self._postorden(nodo.izq)
        self._postorden(nodo.der)
        print(nodo.val)

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
        self._recolectar_descendientes(nodo.izq, valores)
        self._recolectar_descendientes(nodo.der, valores)

        if padre is None:
            self.raiz = None
            for valor in valores:
                self.agregar(valor)
            return

        if padre.izq == nodo:
            padre.izq = None
        elif padre.der == nodo:
            padre.der = None

        for valor in valores:
            self.agregar(valor)

    def _recolectar_descendientes(self, nodo, valores):
        if nodo is None:
            return
        valores.append(nodo.val)
        self._recolectar_descendientes(nodo.izq, valores)
        self._recolectar_descendientes(nodo.der, valores)

    def _actualizar_niveles(self):
        self.altura_max = 0
        self._asignar_niveles(self.raiz, None, 1)

    def _asignar_niveles(self, nodo, prev, nivel):
        if nodo is None:
            return
        nodo.prev = prev
        nodo.altura = nivel
        self.altura_max = max(self.altura_max, nivel)
        self._asignar_niveles(nodo.izq, nodo.val, nivel + 1)
        self._asignar_niveles(nodo.der, nodo.val, nivel + 1)

    def convertir_a_dict(self):
        if not self.raiz:
            return None
        return self._serializar_por_niveles()

    def _serializar_por_niveles(self):
        resultado = []
        fila = [self.raiz]

        while fila:
            siguiente = []
            hay_no_nulos = False

            for nodo in fila:
                if nodo is None:
                    resultado.append(None)
                    siguiente.extend([None, None])
                    continue

                resultado.append({'val': nodo.val})
                siguiente.append(nodo.izq)
                siguiente.append(nodo.der)
                if nodo.izq is not None or nodo.der is not None:
                    hay_no_nulos = True

            if not hay_no_nulos:
                break
            fila = siguiente

        while resultado and resultado[-1] is None:
            resultado.pop()

        return resultado

    def recalcular_metadata(self):
        self._actualizar_niveles()
