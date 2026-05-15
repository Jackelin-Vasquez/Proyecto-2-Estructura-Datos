class Nodo:
    def __init__(self, val):
        self.val = val
        self.izq = None
        self.der = None
        self.altura = 1


class ArbolAVL:
    def __init__(self, nombre):
        self.raiz = None
        self.nombre = nombre

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

        nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))
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

    def rotacion_der(self, nodo):
        new_root = nodo.izq
        temp = new_root.der

        new_root.der = nodo
        nodo.izq = temp

        nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))
        new_root.altura = 1 + max(self.altura(new_root.izq), self.altura(new_root.der))
        return new_root

    def rotacion_izq(self, nodo):
        new_root = nodo.der
        temp = new_root.izq

        new_root.izq = nodo
        nodo.der = temp

        nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))
        new_root.altura = 1 + max(self.altura(new_root.izq), self.altura(new_root.der))
        return new_root

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
        return self._buscar(self.raiz, valor, 1)

    def _buscar(self, nodo, valor, nivel):
        if nodo is None:
            return None
        if valor == nodo.val:
            return nodo.val, nivel
        if valor < nodo.val:
            return self._buscar(nodo.izq, valor, nivel + 1)
        return self._buscar(nodo.der, valor, nivel + 1)

    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.val:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.val:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq

            sucesor = self.min(nodo.der)
            nodo.val = sucesor.val
            nodo.der = self._eliminar(nodo.der, sucesor.val)

        nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))
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

    def min(self, nodo):
        while nodo and nodo.izq:
            nodo = nodo.izq
        return nodo

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
        self._recalcular_alturas(self.raiz)

    def _recalcular_alturas(self, nodo):
        if nodo is None:
            return 0
        altura_izq = self._recalcular_alturas(nodo.izq)
        altura_der = self._recalcular_alturas(nodo.der)
        nodo.altura = 1 + max(altura_izq, altura_der)
        return nodo.altura
