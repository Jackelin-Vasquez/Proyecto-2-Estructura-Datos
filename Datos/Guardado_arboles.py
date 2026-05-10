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