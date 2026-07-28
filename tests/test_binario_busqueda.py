import pytest

from Arboles.binario_busqueda import ArbolBusqueda, Nodo
from tests.helpers import lineas_impresas, valores_por_niveles


@pytest.fixture
def arbol():
    return ArbolBusqueda("abb")


@pytest.fixture
def arbol_lleno():
    a = ArbolBusqueda("abb")
    for valor in [50, 30, 70, 20, 40, 60, 80]:
        a.agregar(valor)
    return a


def test_nodo_inicia_vacio():
    nodo = Nodo(5)
    assert (nodo.val, nodo.izq, nodo.der, nodo.altura) == (5, None, None, 1)


def test_arbol_nuevo_esta_vacio(arbol):
    assert arbol.nombre == "abb"
    assert arbol.raiz is None
    assert arbol.altura_max == 0
    assert arbol.contar_nodos() == 0
    assert arbol.obtener_valor_raiz() is None
    assert arbol.buscar(1) is None
    assert arbol.convertir_a_dict() is None


def test_agregar_raiz(arbol):
    assert arbol.agregar(50) is True
    assert arbol.obtener_valor_raiz() == 50
    assert arbol.raiz.altura == 1
    assert arbol.altura_max == 1


def test_agregar_respeta_orden(arbol_lleno):
    assert valores_por_niveles(arbol_lleno) == [50, 30, 70, 20, 40, 60, 80]
    assert arbol_lleno.altura_max == 3
    assert arbol_lleno.contar_nodos() == 7


def test_agregar_rechaza_duplicado(arbol_lleno, capsys):
    assert arbol_lleno.agregar(30) is False
    assert "duplicado" in capsys.readouterr().out
    assert arbol_lleno.contar_nodos() == 7


def test_agregar_en_rama_izquierda_profunda(arbol):
    for valor in [50, 40, 30, 20]:
        arbol.agregar(valor)
    assert arbol.altura_max == 4
    assert arbol.raiz.izq.izq.izq.val == 20


def test_agregar_en_rama_derecha_profunda(arbol):
    for valor in [50, 60, 70, 80]:
        arbol.agregar(valor)
    assert arbol.altura_max == 4
    assert arbol.raiz.der.der.der.val == 80


def test_buscar_devuelve_valor_y_nivel(arbol_lleno):
    assert arbol_lleno.buscar(50) == (50, 1)
    assert arbol_lleno.buscar(30) == (30, 2)
    assert arbol_lleno.buscar(80) == (80, 3)


def test_buscar_valor_inexistente(arbol_lleno):
    assert arbol_lleno.buscar(99) is None
    assert arbol_lleno.buscar(10) is None


def test_min_devuelve_el_menor(arbol_lleno):
    assert arbol_lleno.min(arbol_lleno.raiz).val == 20
    assert arbol_lleno.min(arbol_lleno.raiz.der).val == 60
    assert arbol_lleno.min(None) is None


def test_recorridos_vacios_no_imprimen(arbol, capsys):
    arbol.preorden()
    arbol.inorden()
    arbol.postorden()
    assert lineas_impresas(capsys) == []


def test_recorridos(arbol_lleno, capsys):
    arbol_lleno.preorden()
    assert lineas_impresas(capsys) == ["50", "30", "20", "40", "70", "60", "80"]

    arbol_lleno.inorden()
    assert lineas_impresas(capsys) == ["20", "30", "40", "50", "60", "70", "80"]

    arbol_lleno.postorden()
    assert lineas_impresas(capsys) == ["20", "40", "30", "60", "80", "70", "50"]


def test_eliminar_hoja(arbol_lleno):
    arbol_lleno.eliminar(20)
    assert valores_por_niveles(arbol_lleno) == [50, 30, 70, 40, 60, 80]
    assert arbol_lleno.altura_max == 3


def test_eliminar_nodo_con_un_hijo_izquierdo(arbol):
    for valor in [50, 30, 20]:
        arbol.agregar(valor)
    arbol.eliminar(30)
    assert valores_por_niveles(arbol) == [50, 20]
    assert arbol.altura_max == 2


def test_eliminar_nodo_con_un_hijo_derecho(arbol):
    for valor in [50, 30, 40]:
        arbol.agregar(valor)
    arbol.eliminar(30)
    assert valores_por_niveles(arbol) == [50, 40]


def test_eliminar_nodo_con_dos_hijos_usa_sucesor(arbol_lleno):
    arbol_lleno.eliminar(30)
    assert valores_por_niveles(arbol_lleno) == [50, 40, 70, 20, 60, 80]


def test_eliminar_raiz(arbol_lleno):
    arbol_lleno.eliminar(50)
    assert arbol_lleno.obtener_valor_raiz() == 60
    assert sorted(valores_por_niveles(arbol_lleno)) == [20, 30, 40, 60, 70, 80]


def test_eliminar_unico_nodo(arbol):
    arbol.agregar(50)
    arbol.eliminar(50)
    assert arbol.raiz is None
    assert arbol.altura_max == 0


def test_eliminar_valor_inexistente_no_cambia_nada(arbol_lleno):
    arbol_lleno.eliminar(99)
    assert valores_por_niveles(arbol_lleno) == [50, 30, 70, 20, 40, 60, 80]


def test_eliminar_actualiza_alturas(arbol):
    for valor in [50, 40, 30, 20]:
        arbol.agregar(valor)
    arbol.eliminar(40)
    assert arbol.altura_max == 3
    assert arbol.buscar(20) == (20, 3)


def test_convertir_a_dict_arbol_completo(arbol_lleno):
    assert arbol_lleno.convertir_a_dict() == [
        {'val': 50}, {'val': 30}, {'val': 70},
        {'val': 20}, {'val': 40}, {'val': 60}, {'val': 80},
    ]


def test_convertir_a_dict_incluye_huecos(arbol):
    for valor in [50, 30, 70, 20]:
        arbol.agregar(valor)
    assert arbol.convertir_a_dict() == [
        {'val': 50}, {'val': 30}, {'val': 70}, {'val': 20},
    ]


def test_convertir_a_dict_rama_derecha(arbol):
    for valor in [50, 70, 80]:
        arbol.agregar(valor)
    assert arbol.convertir_a_dict() == [
        {'val': 50}, None, {'val': 70}, None, None, None, {'val': 80},
    ]


def test_recalcular_metadata_desde_arbol_manual():
    arbol = ArbolBusqueda("manual")
    arbol.raiz = Nodo(50)
    arbol.raiz.izq = Nodo(30)
    arbol.raiz.izq.izq = Nodo(20)
    arbol.recalcular_metadata()
    assert arbol.altura_max == 3
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq.altura == 2
    assert arbol.raiz.izq.izq.altura == 3
