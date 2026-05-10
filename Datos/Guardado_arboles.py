import json
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

    def bn_covert(self, name):
        if not any(k_name == name for k_name in self.conv_origin.binario_n.keys()):
            return False

        obj_instance = self.conv_origin.binario_n[name]
        n_list = obj_instance.convertir_a_dict()

        self.binario_n[name] = {
            "nombre": obj_instance.nombre,
            "altura": obj_instance.altura,
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
            "altura": obj_instance.altura,
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
            "altura": obj_instance.altura,
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


"""
    Formato de referencia:
    arbol = {
        "nombre": ---
        "altura": ---
        "raiz": ---
        "valores": ---
    }
"""