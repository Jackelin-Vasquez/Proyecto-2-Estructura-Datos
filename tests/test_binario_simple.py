import pytest

from Arboles.binario_simple import ArbolSimple, Nodo
from tests.helpers import lineas_impresas, valores_por_niveles


@pytest.fixture
def arbol():
    return ArbolSimple("simple")


@pytest.fixture
def arbol_lleno():
    a = ArbolSimple("simple")
    for valor in [1, 2, 3, 4, 5, 6, 7]:
        a.agregar(valor)
    return a


def test_nodo_inicia_vacio():
    nodo = Nodo(10)
    assert (nodo.val, nodo.izq, nodo.der, nodo.prev, nodo.altura) == (10, None, None, None, 0)


def test_arbol_nuevo_esta_vacio(arbol):
    assert arbol.nombre == "simple"
    assert arbol.raiz is None
    assert arbol.altura_max == 0
    assert arbol.contar_nodos() == 0
    assert arbol.obtener_valor_raiz() is None
    assert arbol.buscar(1) is None
    assert arbol.convertir_a_dict() is None
    assert arbol.eliminar(1) is False


def test_agregar_raiz(arbol):
    assert arbol.agregar(10) is True
    assert arbol.raiz.val == 10
    assert arbol.raiz.altura == 1
    assert arbol.altura_max == 1
    assert arbol.obtener_valor_raiz() == 10


def test_agregar_llena_por_niveles(arbol_lleno):
    assert valores_por_niveles(arbol_lleno) == [1, 2, 3, 4, 5, 6, 7]
    assert arbol_lleno.altura_max == 3
    assert arbol_lleno.contar_nodos() == 7


def test_agregar_asigna_padre_y_nivel(arbol_lleno):
    val, altura, prev = arbol_lleno.buscar(5)
    assert (val, altura, prev) == (5, 3, 2)


def test_agregar_rechaza_duplicados(arbol_lleno):
    assert arbol_lleno.agregar(4) is False
    assert arbol_lleno.contar_nodos() == 7


def test_agregar_crece_a_nuevo_nivel(arbol_lleno):
    assert arbol_lleno.agregar(8) is True
    assert arbol_lleno.altura_max == 4
    assert arbol_lleno.raiz.izq.izq.izq.val == 8


def test_buscar_valor_inexistente(arbol_lleno):
    assert arbol_lleno.buscar(99) is None


def test_recorridos_vacios_no_imprimen(arbol, capsys):
    arbol.preorden()
    arbol.inorden()
    arbol.postorden()
    assert lineas_impresas(capsys) == []


def test_recorridos(arbol_lleno, capsys):
    arbol_lleno.preorden()
    assert lineas_impresas(capsys) == ["1", "2", "4", "5", "3", "6", "7"]

    arbol_lleno.inorden()
    assert lineas_impresas(capsys) == ["4", "2", "5", "1", "6", "3", "7"]

    arbol_lleno.postorden()
    assert lineas_impresas(capsys) == ["4", "5", "2", "6", "7", "3", "1"]


def test_eliminar_hoja(arbol_lleno):
    assert arbol_lleno.eliminar(7) is True
    assert valores_por_niveles(arbol_lleno) == [1, 2, 3, 4, 5, 6]
    assert arbol_lleno.altura_max == 3


def test_eliminar_valor_inexistente(arbol_lleno):
    assert arbol_lleno.eliminar(99) is False
    assert arbol_lleno.contar_nodos() == 7


def test_eliminar_nodo_interno_reinserta_descendientes(arbol_lleno):
    assert arbol_lleno.eliminar(2) is True
    assert arbol_lleno.contar_nodos() == 6
    assert sorted(valores_por_niveles(arbol_lleno)) == [1, 3, 4, 5, 6, 7]
    assert arbol_lleno.obtener_valor_raiz() == 1


def test_eliminar_raiz_reinserta_descendientes(arbol_lleno):
    assert arbol_lleno.eliminar(1) is True
    assert arbol_lleno.contar_nodos() == 6
    assert sorted(valores_por_niveles(arbol_lleno)) == [2, 3, 4, 5, 6, 7]
    assert arbol_lleno.raiz.altura == 1


def test_eliminar_unico_nodo(arbol):
    arbol.agregar(10)
    assert arbol.eliminar(10) is True
    assert arbol.raiz is None
    assert arbol.altura_max == 0


def test_eliminar_actualiza_niveles_y_padres(arbol_lleno):
    arbol_lleno.eliminar(3)
    for valor in valores_por_niveles(arbol_lleno):
        _, altura, prev = arbol_lleno.buscar(valor)
        assert 1 <= altura <= arbol_lleno.altura_max
        assert (prev is None) == (valor == arbol_lleno.obtener_valor_raiz())


def test_convertir_a_dict_arbol_completo(arbol_lleno):
    assert arbol_lleno.convertir_a_dict() == [
        {'val': 1}, {'val': 2}, {'val': 3},
        {'val': 4}, {'val': 5}, {'val': 6}, {'val': 7},
    ]


def test_convertir_a_dict_solo_raiz(arbol):
    arbol.agregar(10)
    assert arbol.convertir_a_dict() == [{'val': 10}]


def test_convertir_a_dict_incluye_huecos(arbol):
    arbol.agregar(1)
    arbol.agregar(2)
    arbol.agregar(3)
    arbol.agregar(4)
    assert arbol.convertir_a_dict() == [{'val': 1}, {'val': 2}, {'val': 3}, {'val': 4}]


def test_convertir_a_dict_con_rama_faltante():
    arbol = ArbolSimple("manual")
    arbol.raiz = Nodo(1)
    arbol.raiz.der = Nodo(3)
    arbol.raiz.der.der = Nodo(7)
    arbol.recalcular_metadata()
    assert arbol.convertir_a_dict() == [
        {'val': 1}, None, {'val': 3}, None, None, None, {'val': 7},
    ]


def test_recalcular_metadata_desde_arbol_manual():
    arbol = ArbolSimple("manual")
    arbol.raiz = Nodo(1)
    arbol.raiz.izq = Nodo(2)
    arbol.raiz.izq.izq = Nodo(4)
    arbol.recalcular_metadata()
    assert arbol.altura_max == 3
    assert arbol.raiz.altura == 1
    assert arbol.raiz.izq.prev == 1
    assert arbol.raiz.izq.izq.altura == 3
    assert arbol.raiz.izq.izq.prev == 2
