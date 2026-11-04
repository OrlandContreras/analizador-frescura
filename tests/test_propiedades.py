"""Lab 4: pruebas basadas en propiedades, derivadas de los requisitos.

En lugar de probar algunos valores elegidos a mano, Hypothesis genera cientos de
entradas y busca un caso que rompa cada propiedad.
"""

from hypothesis import given
from hypothesis import strategies as st

from frescura.catalogo import cargar_catalogo
from frescura.nutricion import nutricion_por_porcion
from frescura.reglas import ETAPAS, dias_hasta_optimo, etapa_madurez

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
