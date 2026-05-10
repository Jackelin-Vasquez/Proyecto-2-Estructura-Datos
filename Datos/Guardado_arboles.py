"""

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