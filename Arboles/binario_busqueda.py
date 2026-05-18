class Nodo:
    def __init__(self, val):
        self.val = val
        self.izq = None
        self.der = None
        self.altura = 1


class ArbolBusqueda:
    def __init__(self, nombre):
        self.raiz = None
        self.nombre = nombre
        self.altura_max = 0

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
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if nodo is None:
            return None
        if valor == nodo.val:
            return nodo.val, nodo.altura
        if valor < nodo.val:
            return self._buscar(nodo.izq, valor)
        return self._buscar(nodo.der, valor)

    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)
        self._actualizar_alturas()

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.val:
            nodo.izq = self._eliminar(nodo.izq, valor)
            return nodo

        if valor > nodo.val:
            nodo.der = self._eliminar(nodo.der, valor)
            return nodo

        if nodo.izq is None:
            return nodo.der
        if nodo.der is None:
            return nodo.izq

        sucesor = self.min(nodo.der)
        nodo.val = sucesor.val
        nodo.der = self._eliminar(nodo.der, sucesor.val)
        return nodo

    def min(self, nodo):
        while nodo and nodo.izq:
            nodo = nodo.izq
        return nodo

    def _actualizar_alturas(self):
        self.altura_max = 0
        self._asignar_alturas(self.raiz, 1)

    def _asignar_alturas(self, nodo, nivel):
        if nodo is None:
            return
        nodo.altura = nivel
        self.altura_max = max(self.altura_max, nivel)
        self._asignar_alturas(nodo.izq, nivel + 1)
        self._asignar_alturas(nodo.der, nivel + 1)

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
        self._actualizar_alturas()

    def obtener_valor_raiz(self):
        if self.raiz:
            return self.raiz.val
        return None

    def contar_nodos(self):
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_nodos(nodo.izq) + self._contar_nodos(nodo.der)