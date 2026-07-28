def valores_por_niveles(arbol):
    """Devuelve los valores del arbol en recorrido por niveles (BFS)."""
    resultado = []
    fila = [arbol.raiz] if arbol.raiz else []
    while fila:
        nodo = fila.pop(0)
        resultado.append(nodo.val)
        if nodo.izq:
            fila.append(nodo.izq)
        if nodo.der:
            fila.append(nodo.der)
    return resultado


def lineas_impresas(capsys):
    salida = capsys.readouterr().out.strip()
    if not salida:
        return []
    return salida.splitlines()
