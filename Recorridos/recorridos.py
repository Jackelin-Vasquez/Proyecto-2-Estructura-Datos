"""Operaciones genéricas sobre nodos binarios (izq / der / val / altura).

Todas las funciones trabajan con cualquier nodo que exponga los atributos
``val``, ``izq`` y ``der``, por lo que son compartidas por los tres tipos de
árbol del sistema.
"""


def preorden(nodo, visitar):
    if nodo is None:
        return
    visitar(nodo.val)
    preorden(nodo.izq, visitar)
    preorden(nodo.der, visitar)


def inorden(nodo, visitar):
    if nodo is None:
        return
    inorden(nodo.izq, visitar)
    visitar(nodo.val)
    inorden(nodo.der, visitar)


def postorden(nodo, visitar):
    if nodo is None:
        return
    postorden(nodo.izq, visitar)
    postorden(nodo.der, visitar)
    visitar(nodo.val)


def contar_nodos(nodo):
    if nodo is None:
        return 0
    return 1 + contar_nodos(nodo.izq) + contar_nodos(nodo.der)


def recolectar_valores(nodo, valores):
    """Agrega en ``valores`` los valores del subárbol en preorden."""
    if nodo is None:
        return valores
    valores.append(nodo.val)
    recolectar_valores(nodo.izq, valores)
    recolectar_valores(nodo.der, valores)
    return valores


def minimo(nodo):
    while nodo and nodo.izq:
        nodo = nodo.izq
    return nodo


def asignar_niveles(nodo, nivel=1, prev=None, asignar_prev=False):
    """Escribe el nivel de cada nodo en ``altura`` y devuelve el nivel máximo.

    Con ``asignar_prev`` también guarda en ``prev`` el valor del padre.
    """
    if nodo is None:
        return 0
    nodo.altura = nivel
    if asignar_prev:
        nodo.prev = prev
    return max(
        nivel,
        asignar_niveles(nodo.izq, nivel + 1, nodo.val, asignar_prev),
        asignar_niveles(nodo.der, nivel + 1, nodo.val, asignar_prev),
    )


def recalcular_alturas(nodo):
    """Recalcula ``altura`` como la altura del subárbol (estilo AVL)."""
    if nodo is None:
        return 0
    nodo.altura = 1 + max(recalcular_alturas(nodo.izq), recalcular_alturas(nodo.der))
    return nodo.altura


def profundidad(nodo):
    if nodo is None:
        return 0
    return 1 + max(profundidad(nodo.izq), profundidad(nodo.der))


def buscar_ordenado(nodo, valor, nivel=1):
    """Búsqueda binaria; devuelve ``(valor, nivel)`` o ``None``."""
    encontrado = nodo_ordenado(nodo, valor)
    if encontrado is None:
        return None
    return encontrado[0].val, nivel + encontrado[1]


def nodo_ordenado(nodo, valor):
    """Busca ``valor`` en un árbol ordenado; devuelve ``(nodo, saltos)``."""
    saltos = 0
    while nodo:
        if valor == nodo.val:
            return nodo, saltos
        nodo = nodo.izq if valor < nodo.val else nodo.der
        saltos += 1
    return None


def camino_ordenado(raiz, valor):
    """Camino de valores recorrido al buscar ``valor`` en un árbol ordenado."""
    camino = []
    nodo = raiz
    while nodo:
        camino.append(nodo.val)
        if valor == nodo.val:
            break
        siguiente = nodo.izq if valor < nodo.val else nodo.der
        if siguiente is None:
            break
        nodo = siguiente
    return camino


def camino_por_niveles(raiz, valor):
    """Camino hasta ``valor`` recorriendo por niveles (árbol no ordenado)."""
    if raiz is None:
        return []
    cola = [(raiz, [raiz.val])]
    while cola:
        nodo, ruta = cola.pop(0)
        if nodo.val == valor:
            return ruta
        if nodo.izq:
            cola.append((nodo.izq, ruta + [nodo.izq.val]))
        if nodo.der:
            cola.append((nodo.der, ruta + [nodo.der.val]))
    return [raiz.val]


def eliminar_ordenado(nodo, valor, reequilibrar=None):
    """Elimina ``valor`` de un árbol ordenado y devuelve la nueva subraíz.

    ``reequilibrar`` se aplica a cada nodo del camino de retorno (lo usa el AVL
    para actualizar alturas y rotar).
    """
    if nodo is None:
        return None

    if valor < nodo.val:
        nodo.izq = eliminar_ordenado(nodo.izq, valor, reequilibrar)
    elif valor > nodo.val:
        nodo.der = eliminar_ordenado(nodo.der, valor, reequilibrar)
    else:
        if nodo.izq is None:
            return nodo.der
        if nodo.der is None:
            return nodo.izq
        sucesor = minimo(nodo.der)
        nodo.val = sucesor.val
        nodo.der = eliminar_ordenado(nodo.der, sucesor.val, reequilibrar)

    if reequilibrar is None:
        return nodo
    return reequilibrar(nodo)


def serializar_por_niveles(raiz):
    """Serializa el árbol como lista por niveles (heap) de ``{'val': ...}``."""
    if raiz is None:
        return None

    resultado = []
    fila = [raiz]

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
