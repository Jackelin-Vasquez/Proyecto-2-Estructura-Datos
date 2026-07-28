"""Registro único de los tipos de árbol del sistema.

Cada tipo se identifica con una clave ("simple", "busqueda", "avl") y desde
aquí se obtiene su clase de árbol, su clase de nodo, el archivo JSON donde se
persiste y la etiqueta que muestra la interfaz. Sustituye las cadenas de
``if tipo == ...`` repartidas por el sistema.
"""

from Arboles.binario_balanceado import ArbolAVL, Nodo as NodoAVL
from Arboles.binario_busqueda import ArbolBusqueda, Nodo as NodoBusqueda
from Arboles.binario_simple import ArbolSimple, Nodo as NodoSimple

SIMPLE = "simple"
BUSQUEDA = "busqueda"
AVL = "avl"


class TipoArbol:
    def __init__(self, clave, etiqueta, archivo, arbol_clase, nodo_clase):
        self.clave = clave
        self.etiqueta = etiqueta
        self.archivo = archivo
        self.arbol_clase = arbol_clase
        self.nodo_clase = nodo_clase


TIPOS = {
    SIMPLE: TipoArbol(SIMPLE, "Árbol binario", "binario_simple.json", ArbolSimple, NodoSimple),
    BUSQUEDA: TipoArbol(BUSQUEDA, "Árbol BST", "binario_busqueda.json", ArbolBusqueda, NodoBusqueda),
    AVL: TipoArbol(AVL, "Árbol AVL", "binario_balanceado.json", ArbolAVL, NodoAVL),
}
