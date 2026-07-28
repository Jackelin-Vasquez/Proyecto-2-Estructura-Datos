import json

from Datos.tipos_arbol import AVL, BUSQUEDA, SIMPLE, TIPOS

"""
    Sistema de guardado JSON y de conversión de los arbolitos.
    Los tres tipos de árbol comparten el mismo flujo, así que las operaciones
    son genéricas y se seleccionan con la clave del tipo (ver Datos.tipos_arbol).
"""


class ArbolesRaw:
    """
    SOLO SE DEBE LLAMAR A ESTA CLASE UNA VEZ EN TO-DO EL SISTEMA.
    Aquí se guardan los árboles en formato de diccionarios (por eso formato RAW).
    Este espacio de guardado se encarga de ser el intermediario inmediato entre los JSON y las estructuras del sistema.
    """
    def __init__(self):
        self.conv_origin = None
        self.binario_n = {}
        self.binario_ABB = {}
        self.binario_AVB = {}
        # Los diccionarios se mutan, nunca se reasignan, para que este índice siga siendo válido.
        self.por_tipo = {
            SIMPLE: self.binario_n,
            BUSQUEDA: self.binario_ABB,
            AVL: self.binario_AVB,
        }

    def _obtener_altura(self, obj_instance):
        if hasattr(obj_instance, "altura_max"):
            return obj_instance.altura_max
        if hasattr(obj_instance, "raiz"):
            return obj_instance.raiz.altura if obj_instance.raiz else 0
        return None

    def convertir(self, tipo, name):
        instancias = self.conv_origin.por_tipo[tipo]
        if name not in instancias:
            return False

        obj_instance = instancias[name]
        self.por_tipo[tipo][name] = {
            "nombre": obj_instance.nombre,
            "altura": self._obtener_altura(obj_instance),
            "valores": obj_instance.convertir_a_dict()
        }
        return True

    def guardar(self, tipo):
        for nombre in list(self.conv_origin.por_tipo[tipo].keys()):
            self.convertir(tipo, nombre)

        with open(TIPOS[tipo].archivo, 'w', encoding='utf-8') as c:
            json.dump(self.por_tipo[tipo], c, ensure_ascii=False, indent=4)
        return True

    def full_save(self):
        for tipo in TIPOS:
            self.guardar(tipo)

    def load(self):
        for tipo, spec in TIPOS.items():
            with open(spec.archivo, 'r', encoding='utf-8') as c:
                self.por_tipo[tipo].clear()
                self.por_tipo[tipo].update(json.load(c))


class ArbolesConv:
    """
    SOLO SE DEBE LLAMAR A ESTA CLASE UNA VEZ EN TO-DO EL SISTEMA.
    Aquí se guardan los árboles en el formato del sistema (básicamente instancias de los árboles).
    Este punto funciona como punto de guardado de los árboles instanciados: un pequeño caché local para acceder rápidamente a los árboles convertidos a los formatos que el sistema principal trabaja.
    """
    def __init__(self):
        self.raw_origin = None
        # se guardan los árboles
        # CLAVE: nombre del árbol (no se puede repetir)
        # VALOR: instancia del árbol
        self.binario_n = {}
        self.binario_ABB = {}
        self.binario_AVB = {}
        self.por_tipo = {
            SIMPLE: self.binario_n,
            BUSQUEDA: self.binario_ABB,
            AVL: self.binario_AVB,
        }

    def _extraer_valores(self, raw_tree):
        if not raw_tree:
            return []

        valores = raw_tree.get("valores", [])
        if valores is None:
            return []

        if isinstance(valores, dict):
            valores = list(valores.values())

        if not isinstance(valores, list):
            return []

        clean_values = []
        for nodo in valores:
            if isinstance(nodo, dict):
                clean_values.append(nodo["val"] if "val" in nodo else None)
            else:
                clean_values.append(nodo)
        return clean_values

    def _crear_nodo(self, item, node_class):
        if item is None:
            return None
        if isinstance(item, dict):
            if "val" not in item:
                return None
            return node_class(item["val"])
        return node_class(item)

    def _reconstruir_desde_niveles(self, tree_instance, niveles, node_class):
        if not niveles:
            return tree_instance

        nodos = [self._crear_nodo(item, node_class) for item in niveles]
        if not nodos or nodos[0] is None:
            tree_instance.raiz = None
            return tree_instance

        for i, nodo in enumerate(nodos):
            if nodo is None:
                continue
            hijo_izq = (2 * i) + 1
            hijo_der = (2 * i) + 2
            if hijo_izq < len(nodos):
                nodo.izq = nodos[hijo_izq]
            if hijo_der < len(nodos):
                nodo.der = nodos[hijo_der]

        tree_instance.raiz = nodos[0]
        tree_instance.recalcular_metadata()
        return tree_instance

    def convertir(self, tipo, name):
        raw_dict = self.raw_origin.por_tipo[tipo]
        if name not in raw_dict:
            return False

        spec = TIPOS[tipo]
        raw_tree = raw_dict[name]
        tree_instance = spec.arbol_clase(raw_tree.get("nombre", name))
        niveles = self._extraer_valores(raw_tree)

        self.por_tipo[tipo][name] = self._reconstruir_desde_niveles(
            tree_instance, niveles, spec.nodo_clase
        )
        return True

    def dump(self, tipo):
        for nombre in list(self.raw_origin.por_tipo[tipo].keys()):
            self.convertir(tipo, nombre)
        return True

    def full_dump(self):
        for tipo in TIPOS:
            self.dump(tipo)

    def search(self, tipo, name):
        local_dict = self.por_tipo[tipo]
        if name in local_dict:
            return local_dict[name]

        if self.raw_origin is None:
            return False

        if not self.convertir(tipo, name):
            return False

        return local_dict.get(name, False)

    def registrar(self, tipo, arbol):
        """Guarda una instancia recién creada en el caché local."""
        self.por_tipo[tipo][arbol.nombre] = arbol
        return arbol


"""
    Formato de referencia:
    arbol = {
        "nombre": ---
        "altura": ---
        "raiz": ---
        "valores": ---
    }
"""
