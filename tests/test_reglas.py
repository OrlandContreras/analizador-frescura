import pytest

from frescura.catalogo import obtener_producto
from frescura.reglas import dias_hasta_optimo, etapa_madurez

BANANO = obtener_producto("banano")  # umbrales: pinton 25, maduro 50, sobremaduro 80


@pytest.mark.parametrize(
    ("indice", "etapa"),
    [(0, "verde"), (24, "verde"), (25, "pinton"), (49, "pinton"), (50, "maduro"), (79, "maduro"), (95, "sobremaduro")],
)
def test_etapa_segun_indice(indice, etapa):
    assert etapa_madurez(indice, BANANO["umbrales"]) == etapa


# Lab 4: esta prueba describe el comportamiento esperado y falla hasta corregir el error.
def test_umbral_exacto_de_sobremaduro_ya_es_sobremaduro():
    assert etapa_madurez(80, BANANO["umbrales"]) == "sobremaduro"


def test_dias_hasta_optimo_redondea_hacia_arriba():
    # Faltan 50 - 20 = 30 puntos; a 12 por día son 2,5 días -> 3.
    assert dias_hasta_optimo(20, BANANO["umbrales"], BANANO["velocidad_maduracion_dia"]) == 3


def test_dias_hasta_optimo_es_cero_si_ya_esta_maduro():
    assert dias_hasta_optimo(70, BANANO["umbrales"], BANANO["velocidad_maduracion_dia"]) == 0
