import json

import pytest

from Arboles.binario_balanceado import ArbolAVL
from Arboles.binario_busqueda import ArbolBusqueda
from Arboles.binario_simple import ArbolSimple
from Datos.Guardado_arboles import ArbolesConv, ArbolesRaw
from tests.helpers import valores_por_niveles


def construir(tree_class, valores, nombre="arbol"):
    arbol = tree_class(nombre)
    for valor in valores:
        arbol.agregar(valor)
    return arbol


@pytest.fixture
def almacenes():
    raw = ArbolesRaw()
    conv = ArbolesConv()
    raw.conv_origin = conv
    conv.raw_origin = raw
    return raw, conv


@pytest.fixture
def almacenes_con_arboles(almacenes):
    raw, conv = almacenes
    conv.binario_n["simple"] = construir(ArbolSimple, [1, 2, 3], "simple")
    conv.binario_ABB["abb"] = construir(ArbolBusqueda, [50, 30, 70], "abb")
    conv.binario_AVB["avl"] = construir(ArbolAVL, [50, 30, 70], "avl")
    return raw, conv


def test_raw_inicia_vacio(almacenes):
    raw, _ = almacenes
    assert raw.binario_n == {}
    assert raw.binario_ABB == {}
    assert raw.binario_AVB == {}


def test_obtener_altura_usa_altura_max(almacenes):
    raw, _ = almacenes
    arbol = construir(ArbolSimple, [1, 2, 3])
    assert raw._obtener_altura(arbol) == 2


def test_obtener_altura_usa_raiz_cuando_no_hay_altura_max(almacenes):
    raw, _ = almacenes
    arbol = construir(ArbolAVL, [50, 30, 70])
    assert raw._obtener_altura(arbol) == 2


def test_obtener_altura_de_arbol_vacio_sin_altura_max(almacenes):
    raw, _ = almacenes
    assert raw._obtener_altura(ArbolAVL("vacio")) == 0


def test_obtener_altura_de_objeto_con_atributo_altura(almacenes):
    raw, _ = almacenes

    class Falso:
        altura = 7

    assert raw._obtener_altura(Falso()) == 7


def test_obtener_altura_sin_informacion(almacenes):
    raw, _ = almacenes
    assert raw._obtener_altura(object()) is None


@pytest.mark.parametrize(
    "metodo, atributo, nombre",
    [
        ("bn_convert", "binario_n", "simple"),
        ("bABB_convert", "binario_ABB", "abb"),
        ("bAVB_convert", "binario_AVB", "avl"),
    ],
)
def test_convert_guarda_formato_raw(almacenes_con_arboles, metodo, atributo, nombre):
    raw, _ = almacenes_con_arboles
    assert getattr(raw, metodo)(nombre) is True

    entrada = getattr(raw, atributo)[nombre]
    assert entrada["nombre"] == nombre
    assert entrada["altura"] == 2
    assert entrada["valores"][0]["val"] == (1 if nombre == "simple" else 50)


@pytest.mark.parametrize(
    "metodo", ["bn_convert", "bABB_convert", "bAVB_convert"]
)
def test_convert_de_nombre_inexistente(almacenes_con_arboles, metodo):
    raw, _ = almacenes_con_arboles
    assert getattr(raw, metodo)("desconocido") is False


def test_save_escribe_json(almacenes_con_arboles, tmp_path, monkeypatch):
    raw, _ = almacenes_con_arboles
    monkeypatch.chdir(tmp_path)

    assert raw.bn_save() is True
    assert raw.bABB_save() is True
    assert raw.bAVB_save() is True

    datos = json.loads((tmp_path / "binario_simple.json").read_text(encoding="utf-8"))
    assert datos["simple"]["valores"] == [{"val": 1}, {"val": 2}, {"val": 3}]
    assert (tmp_path / "binario_busqueda.json").exists()
    assert (tmp_path / "binario_balanceado.json").exists()


def test_full_save_y_load_ida_y_vuelta(almacenes_con_arboles, tmp_path, monkeypatch):
    raw, _ = almacenes_con_arboles
    monkeypatch.chdir(tmp_path)
    raw.full_save()

    otro = ArbolesRaw()
    otro.load()
    assert otro.binario_n["simple"]["nombre"] == "simple"
    assert otro.binario_ABB["abb"]["valores"] == [{"val": 50}, {"val": 30}, {"val": 70}]
    assert otro.binario_AVB["avl"]["altura"] == 2


def test_extraer_valores_de_lista(almacenes):
    _, conv = almacenes
    raw_tree = {"valores": [{"val": 1}, None, {"val": 3}, 4]}
    assert conv._extraer_valores(raw_tree) == [1, None, 3, 4]


def test_extraer_valores_de_dict(almacenes):
    _, conv = almacenes
    raw_tree = {"valores": {"0": {"val": 1}, "1": 2, "2": None}}
    assert conv._extraer_valores(raw_tree) == [1, 2]


def test_extraer_valores_casos_vacios(almacenes):
    _, conv = almacenes
    assert conv._extraer_valores(None) == []
    assert conv._extraer_valores({}) == []
    assert conv._extraer_valores({"valores": None}) == []
    assert conv._extraer_valores({"valores": "texto"}) == []


def test_crear_nodo(almacenes):
    from Arboles.binario_simple import Nodo as NodoSimple

    _, conv = almacenes
    assert conv._crear_nodo(None, NodoSimple) is None
    assert conv._crear_nodo({"sin_val": 1}, NodoSimple) is None
    assert conv._crear_nodo({"val": 9}, NodoSimple).val == 9
    assert conv._crear_nodo(9, NodoSimple).val == 9


def test_reconstruir_desde_niveles_vacio(almacenes):
    from Arboles.binario_simple import Nodo as NodoSimple

    _, conv = almacenes
    arbol = ArbolSimple("vacio")
    assert conv._reconstruir_desde_niveles(arbol, [], NodoSimple) is arbol
    assert arbol.raiz is None


def test_reconstruir_sin_raiz_deja_arbol_vacio(almacenes):
    from Arboles.binario_simple import Nodo as NodoSimple

    _, conv = almacenes
    arbol = ArbolSimple("vacio")
    reconstruido = conv._reconstruir_desde_niveles(arbol, [None, 2, 3], NodoSimple)
    assert reconstruido.raiz is None


def test_reconstruir_enlaza_hijos_y_recalcula(almacenes):
    from Arboles.binario_simple import Nodo as NodoSimple

    _, conv = almacenes
    arbol = conv._reconstruir_desde_niveles(
        ArbolSimple("simple"), [1, 2, 3, None, 5], NodoSimple
    )
    assert valores_por_niveles(arbol) == [1, 2, 3, 5]
    assert arbol.altura_max == 3
    assert arbol.raiz.der.val == 3


@pytest.mark.parametrize(
    "metodo, atributo, tipo",
    [
        ("bn_convert", "binario_n", ArbolSimple),
        ("bABB_convert", "binario_ABB", ArbolBusqueda),
        ("bAVB_convert", "binario_AVB", ArbolAVL),
    ],
)
def test_conv_convert_reconstruye_instancia(almacenes, metodo, atributo, tipo):
    raw, conv = almacenes
    getattr(raw, atributo)["x"] = {
        "nombre": "x",
        "altura": 2,
        "valores": [{"val": 50}, {"val": 30}, {"val": 70}],
    }

    assert getattr(conv, metodo)("x") is True
    arbol = getattr(conv, atributo)["x"]
    assert isinstance(arbol, tipo)
    assert arbol.nombre == "x"
    assert valores_por_niveles(arbol) == [50, 30, 70]


@pytest.mark.parametrize("metodo", ["bn_convert", "bABB_convert", "bAVB_convert"])
def test_conv_convert_de_nombre_inexistente(almacenes, metodo):
    _, conv = almacenes
    assert getattr(conv, metodo)("desconocido") is False


@pytest.mark.parametrize(
    "metodo_dump, atributo",
    [
        ("bn_dump", "binario_n"),
        ("bABB_dump", "binario_ABB"),
        ("bAVB_dump", "binario_AVB"),
    ],
)
def test_dump_convierte_todos_los_arboles(almacenes, metodo_dump, atributo):
    raw, conv = almacenes
    for nombre in ["a", "b"]:
        getattr(raw, atributo)[nombre] = {
            "nombre": nombre,
            "altura": 1,
            "valores": [{"val": 1}],
        }

    assert getattr(conv, metodo_dump)() is True
    assert sorted(getattr(conv, atributo).keys()) == ["a", "b"]


@pytest.mark.parametrize(
    "metodo_search, atributo",
    [
        ("bn_search", "binario_n"),
        ("bABB_search", "binario_ABB"),
        ("bAVB_search", "binario_AVB"),
    ],
)
def test_search_devuelve_instancia_en_cache(almacenes_con_arboles, metodo_search, atributo):
    _, conv = almacenes_con_arboles
    nombre = next(iter(getattr(conv, atributo)))
    assert getattr(conv, metodo_search)(nombre) is getattr(conv, atributo)[nombre]


@pytest.mark.parametrize(
    "metodo_search, atributo",
    [
        ("bn_search", "binario_n"),
        ("bABB_search", "binario_ABB"),
        ("bAVB_search", "binario_AVB"),
    ],
)
def test_search_convierte_desde_raw(almacenes, metodo_search, atributo):
    raw, conv = almacenes
    getattr(raw, atributo)["x"] = {
        "nombre": "x",
        "altura": 1,
        "valores": [{"val": 10}],
    }

    arbol = getattr(conv, metodo_search)("x")
    assert arbol is not False
    assert arbol.obtener_valor_raiz() == 10
    assert "x" in getattr(conv, atributo)


@pytest.mark.parametrize(
    "metodo_search", ["bn_search", "bABB_search", "bAVB_search"]
)
def test_search_sin_resultado(almacenes, metodo_search):
    _, conv = almacenes
    assert getattr(conv, metodo_search)("desconocido") is False


def test_search_en_dicts_cuando_falla_la_conversion(almacenes):
    _, conv = almacenes
    raw_dict = {"x": {"nombre": "x", "altura": 1, "valores": []}}
    assert conv._search_en_dicts({}, raw_dict, "x", lambda name: False) is False


@pytest.mark.parametrize(
    "metodo_search", ["bn_search", "bABB_search", "bAVB_search"]
)
def test_search_sin_origen_raw(metodo_search):
    conv = ArbolesConv()
    assert getattr(conv, metodo_search)("cualquiera") is False
