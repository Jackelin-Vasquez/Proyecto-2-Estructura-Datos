import json
from Arboles.__init__ import ArbolBusqueda, ArbolAVL, ArbolSimple
from Arboles.binario_simple import Nodo as NodoSimple
from Arboles.binario_busqueda import Nodo as NodoBusqueda
from Arboles.binario_balanceado import Nodo as NodoAVL

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
        if hasattr(obj_instance, "raiz"):
            return obj_instance.raiz.altura if obj_instance.raiz else 0
        if hasattr(obj_instance, "altura") and not callable(obj_instance.altura):
            return obj_instance.altura
        return None

    def bn_convert(self, name):
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

    def bABB_convert(self, name):
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

    def bAVB_convert(self, name):
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
            self.bn_convert(bn_tree)

        with open('binario_simple.json', 'w', encoding='utf-8') as c:
            json.dump(self.binario_n, c, ensure_ascii=False, indent=4)
        return True


    def bABB_save(self):
        for bABB_tree in self.conv_origin.binario_ABB.keys():
            self.bABB_convert(bABB_tree)

        with open('binario_busqueda.json', 'w', encoding='utf-8') as c:
            json.dump(self.binario_ABB, c, ensure_ascii=False, indent=4)
        return True


    def bAVB_save(self):
        for bAVB_tree in self.conv_origin.binario_AVB.keys():
            self.bAVB_convert(bAVB_tree)

        with open('binario_balanceado.json', 'w', encoding='utf-8') as c:
            json.dump(self.binario_AVB, c, ensure_ascii=False, indent=4)
        return True

    def full_save(self):
        self.bn_save()
        self.bABB_save()
        self.bAVB_save()


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
                elif nodo is None:
                    clean_values.append(None)
                else:
                    clean_values.append(nodo)
            return clean_values

        return []

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
        if hasattr(tree_instance, "recalcular_metadata"):
            tree_instance.recalcular_metadata()
        return tree_instance

    def _convertir_arbol(self, raw_dict, name, tree_class, node_class):
        if not any(k_name == name for k_name in raw_dict.keys()):
            return False

        raw_tree = raw_dict[name]
        tree_instance = tree_class(raw_tree.get("nombre", name))
        niveles = self._extraer_valores(raw_tree)
        return self._reconstruir_desde_niveles(tree_instance, niveles, node_class)

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
        tree_instance = self._convertir_arbol(self.raw_origin.binario_n, name, ArbolSimple, NodoSimple)
        if tree_instance is False:
            return False

        self.binario_n[name] = tree_instance
        return True

    def bABB_convert(self, name):
        tree_instance = self._convertir_arbol(self.raw_origin.binario_ABB, name, ArbolBusqueda, NodoBusqueda)
        if tree_instance is False:
            return False

        self.binario_ABB[name] = tree_instance
        return True

    def bAVB_convert(self, name):
        tree_instance = self._convertir_arbol(self.raw_origin.binario_AVB, name, ArbolAVL, NodoAVL)
        if tree_instance is False:
            return False

        self.binario_AVB[name] = tree_instance
        return True

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
