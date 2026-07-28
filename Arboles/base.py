from Recorridos import recorridos


class NodoBase:
    def __init__(self, val, altura=1):
        self.val = val
        self.izq = None
        self.der = None
        self.altura = altura


class ArbolBase:
    """Comportamiento común a los tres árboles del sistema.

    Los recorridos, la serialización y las consultas de metadata son idénticos
    para todos, así que viven aquí y se apoyan en ``Recorridos.recorridos``.
    """

    def __init__(self, nombre):
        self.raiz = None
        self.nombre = nombre

    def preorden(self):
        recorridos.preorden(self.raiz, print)

    def inorden(self):
        recorridos.inorden(self.raiz, print)

    def postorden(self):
        recorridos.postorden(self.raiz, print)

    def min(self, nodo):
        return recorridos.minimo(nodo)

    def convertir_a_dict(self):
        return recorridos.serializar_por_niveles(self.raiz)

    def contar_nodos(self):
        return recorridos.contar_nodos(self.raiz)

    def obtener_valor_raiz(self):
        if self.raiz:
            return self.raiz.val
        return None

    def recalcular_metadata(self):
        raise NotImplementedError


class ArbolPorNiveles(ArbolBase):
    """Árbol cuya ``altura`` de nodo es el nivel y que cachea ``altura_max``."""

    asignar_prev = False

    def __init__(self, nombre):
        super().__init__(nombre)
        self.altura_max = 0

    def _actualizar_niveles(self):
        self.altura_max = recorridos.asignar_niveles(
            self.raiz, 1, None, self.asignar_prev
        )

    def recalcular_metadata(self):
        self._actualizar_niveles()
