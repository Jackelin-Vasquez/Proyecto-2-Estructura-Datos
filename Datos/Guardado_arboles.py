import json
from Arboles.__init__ import ArbolBusqueda, ArbolAVL, ArbolSimple

"""
    TODO sistema de guardado de JSON para cada tipo de árbol
    TODO sistema de conversión de los arbolitos
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

    def _obtener_altura(self, obj_instance):
        if hasattr(obj_instance, "altura_max"):
            return obj_instance.altura_max
        if hasattr(obj_instance, "altura"):
            return obj_instance.altura
        return None

    def bn_covert(self, name):
        if not any(k_name == name for k_name in self.conv_origin.binario_n.keys()):
            return False

        obj_instance = self.conv_origin.binario_n[name]
        n_list = obj_instance.convertir_a_dict()

        self.binario_n[name] = {
            "nombre": obj_instance.nombre,
            "altura": self._obtener_altura(obj_instance),
            "valores": n_list
        }
        return True

    def bABB_covert(self, name):
        if not any(k_name == name for k_name in self.conv_origin.binario_ABB.keys()):
            return False

        obj_instance = self.conv_origin.binario_ABB[name]
        n_list = obj_instance.convertir_a_dict()

        self.binario_ABB[name] = {
            "nombre": obj_instance.nombre,
            "altura": self._obtener_altura(obj_instance),
            "valores": n_list
        }
        return True

    def bAVB_covert(self, name):
        if not any(k_name == name for k_name in self.conv_origin.binario_AVB.keys()):
            return False

        obj_instance = self.conv_origin.binario_AVB[name]
        n_list = obj_instance.convertir_a_dict()

        self.binario_AVB[name] = {
            "nombre": obj_instance.nombre,
            "altura": self._obtener_altura(obj_instance),
            "valores": n_list
        }
        return True


    def bn_save(self):
        for bn_tree in self.conv_origin.binario_n.keys():
            self.bn_covert(bn_tree)

        with open('binario_simple.json', 'w', encoding='utf-8') as c:
            json.dump(self.binario_n, c, ensure_ascii=False, indent=4)

        return True

    def bABB_save(self):
        for bABB_tree in self.conv_origin.binario_ABB.keys():
            self.bABB_covert(bABB_tree)

        with open('binario_busqueda.json', 'w', encoding='utf-8') as c:
            json.dump(self.binario_ABB, c, ensure_ascii=False, indent=4)
        return True

    def bAVB_save(self):
        for bAVB_tree in self.conv_origin.binario_AVB.keys():
            self.bAVB_covert(bAVB_tree)

        with open('binario_balanceado.json', 'w', encoding='utf-8') as c:
            json.dump(self.binario_AVB, c, ensure_ascii=False, indent=4)
        return True


    def load(self):
        with open('binario_simple.json', 'r', encoding='utf-8') as c:
            self.binario_n = json.load(c)

        with open('binario_busqueda.json', 'r', encoding='utf-8') as c:
            self.binario_ABB = json.load(c)

        with open('binario_balanceado.json', 'r', encoding='utf-8') as c:
            self.binario_AVB = json.load(c)



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


    def _extraer_valores(self, raw_tree):
        if not raw_tree:
            return []

        valores = raw_tree.get("valores", [])
        if valores is None:
            return []

        if isinstance(valores, dict):
            clean_values = []
            for nodo in valores.values():
                if isinstance(nodo, dict) and "val" in nodo:
                    clean_values.append(nodo["val"])
                elif nodo is not None:
                    clean_values.append(nodo)
            return clean_values

        if isinstance(valores, list):
            clean_values = []
            for nodo in valores:
                if isinstance(nodo, dict) and "val" in nodo:
                    clean_values.append(nodo["val"])
                elif nodo is not None:
                    clean_values.append(nodo)
            return clean_values

        return []

    def _convertir_arbol(self, raw_dict, name, tree_class):
        if not any(k_name == name for k_name in raw_dict.keys()):
            return False

        raw_tree = raw_dict[name]
        tree_instance = tree_class(raw_tree.get("nombre", name))

        for valor in self._extraer_valores(raw_tree):
            tree_instance.agregar(valor)

        return tree_instance

    def _search_en_dicts(self, local_dict, raw_dict, name, convert_method):
        if name in local_dict:
            return local_dict[name]

        if raw_dict is None:
            return False

        if name not in raw_dict:
            return False

        convertido = convert_method(name)
        if not convertido:
            return False

        return local_dict.get(name, False)

    def bn_convert(self, name):
        tree_instance = self._convertir_arbol(self.raw_origin.binario_n, name, ArbolSimple)
        if tree_instance is False:
            return False

        self.binario_n[name] = tree_instance
        return True

    def bABB_convert(self, name):
        tree_instance = self._convertir_arbol(self.raw_origin.binario_ABB, name, ArbolBusqueda)
        if tree_instance is False:
            return False

        self.binario_ABB[name] = tree_instance
        return True

    def bAVB_convert(self, name):
        tree_instance = self._convertir_arbol(self.raw_origin.binario_AVB, name, ArbolAVL)
        if tree_instance is False:
            return False

        self.binario_AVB[name] = tree_instance
        return True

    def bn_covert(self, name):
        return self.bn_convert(name)

    def bABB_covert(self, name):
        return self.bABB_convert(name)

    def bAVB_covert(self, name):
        return self.bAVB_convert(name)

    def bn_dump(self):
        for bn_tree in self.raw_origin.binario_n.keys():
            self.bn_convert(bn_tree)
        return True

    def bABB_dump(self):
        for bABB_tree in self.raw_origin.binario_ABB.keys():
            self.bABB_convert(bABB_tree)
        return True

    def bAVB_dump(self):
        for bAVB_tree in self.raw_origin.binario_AVB.keys():
            self.bAVB_convert(bAVB_tree)
        return True

    def bn_search(self, name):
        raw_dict = self.raw_origin.binario_n if self.raw_origin else None
        return self._search_en_dicts(self.binario_n, raw_dict, name, self.bn_convert)

    def bABB_search(self, name):
        raw_dict = self.raw_origin.binario_ABB if self.raw_origin else None
        return self._search_en_dicts(self.binario_ABB, raw_dict, name, self.bABB_convert)

    def bAVB_search(self, name):
        raw_dict = self.raw_origin.binario_AVB if self.raw_origin else None
        return self._search_en_dicts(self.binario_AVB, raw_dict, name, self.bAVB_convert)


"""
    Formato de referencia:
    arbol = {
        "nombre": ---
        "altura": ---
        "raiz": ---
        "valores": ---
    }
"""
