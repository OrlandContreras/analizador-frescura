"""Lab 4: pruebas basadas en propiedades, derivadas de los requisitos.

En lugar de probar algunos valores elegidos a mano, Hypothesis genera cientos de
entradas y busca un caso que rompa cada propiedad.
"""

from hypothesis import given
from hypothesis import strategies as st

from frescura.analizador import analizar_foto
from frescura.catalogo import cargar_catalogo
from frescura.nutricion import nutricion_por_porcion
from frescura.reglas import ETAPAS, dias_hasta_optimo, etapa_madurez
from frescura.vision import LecturaVision
from frescura.vista_cliente import para_cliente

productos = st.sampled_from(list(cargar_catalogo().values()))
indices = st.floats(min_value=0, max_value=100, allow_nan=False)


@given(productos, indices, indices)
def test_mas_indice_nunca_es_menos_maduro(producto, a, b):
    """La etapa nunca retrocede cuando el índice de madurez aumenta."""
    menor, mayor = sorted((a, b))
    umbrales = producto["umbrales"]
    assert ETAPAS.index(etapa_madurez(menor, umbrales)) <= ETAPAS.index(etapa_madurez(mayor, umbrales))


@given(productos)
def test_cada_umbral_pertenece_a_su_etapa(producto):
    """Un índice igual a un umbral ya pertenece a la etapa que ese umbral inicia."""
    umbrales = producto["umbrales"]
    for etapa in ("pinton", "maduro", "sobremaduro"):
        assert etapa_madurez(umbrales[etapa], umbrales) == etapa


@given(productos, indices)
def test_maduro_o_mas_no_tiene_dias_pendientes(producto, indice):
    """Si ya está maduro o sobremaduro faltan 0 días; si no, falta al menos 1."""
    umbrales = producto["umbrales"]
    dias = dias_hasta_optimo(indice, umbrales, producto["velocidad_maduracion_dia"])
    if etapa_madurez(indice, umbrales) in ("maduro", "sobremaduro"):
        assert dias == 0
    else:
        assert dias >= 1


@given(productos, st.floats(min_value=1, max_value=1000, allow_nan=False))
def test_la_nutricion_escala_en_proporcion_a_los_gramos(producto, gramos):
    """El doble de gramos da el doble de energía (con tolerancia por redondeo)."""
    simple = nutricion_por_porcion(producto["id"], gramos)
    doble = nutricion_por_porcion(producto["id"], gramos * 2)
    assert abs(doble["energia_kcal"] - 2 * simple["energia_kcal"]) <= 0.2


class VisionFija:
    """Visión de prueba que devuelve siempre la misma lectura."""

    def __init__(self, lectura: LecturaVision):
        self.lectura = lectura

    def analizar(self, imagen: bytes, formato: str) -> LecturaVision:
        return self.lectura


lecturas = st.builds(
    LecturaVision,
    producto=st.sampled_from([*cargar_catalogo().keys(), "pitahaya"]),
    indice_madurez=indices,
    manchas_pct=st.floats(min_value=0, max_value=100, allow_nan=False),
    defectos=st.lists(st.sampled_from(["moho", "zonas_hundidas", "golpes"]), unique=True),
    confianza=st.floats(min_value=0, max_value=1, allow_nan=False),
)


@given(lecturas)
def test_la_vista_del_cliente_nunca_muestra_informacion_interna(lectura):
    vista = para_cliente(analizar_foto(VisionFija(lectura), b"foto", "jpeg"))
    assert "accion" not in vista and "lectura" not in vista
    assert vista["reconocido"] == (lectura.producto != "pitahaya" and lectura.confianza >= 0.70)
