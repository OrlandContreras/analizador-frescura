"""Pruebas de la política POL-FRV-001: una por regla, en el orden de la política."""

import pytest

from frescura.acciones import recomendar_accion
from frescura.catalogo import obtener_producto
from frescura.vision import LecturaVision

MANGO = obtener_producto("mango")


def lectura(confianza=0.9, manchas=0, defectos=None):
    return LecturaVision("mango", 60, manchas, defectos or [], confianza)


def test_regla_1_confianza_baja_va_a_revision():
    accion = recomendar_accion(lectura(confianza=0.69), "maduro", MANGO)
    assert accion["tipo"] == "revisar"
    assert accion["requiere_confirmacion"] is True


def test_regla_1_producto_desconocido_va_a_revision():
    assert recomendar_accion(lectura(), None, None)["tipo"] == "revisar"


def test_regla_1_confianza_exacta_de_070_no_va_a_revision():
    assert recomendar_accion(lectura(confianza=0.70), "maduro", MANGO)["tipo"] == "priorizar"


def test_regla_2_moho_se_retira_aunque_este_verde():
    assert recomendar_accion(lectura(defectos=["moho"]), "verde", MANGO)["tipo"] == "retirar"


@pytest.mark.parametrize("etapa", ["verde", "pinton"])
def test_regla_3_verde_o_pinton_se_mantiene(etapa):
    assert recomendar_accion(lectura(), etapa, MANGO)["tipo"] == "mantener"


def test_regla_4_maduro_se_prioriza():
    assert recomendar_accion(lectura(), "maduro", MANGO)["tipo"] == "priorizar"


@pytest.mark.parametrize(
    ("manchas", "defectos", "tipo"),
    [
        (29, [], "rebajar"),
        (30, [], "transformar"),
        (10, ["zonas_hundidas"], "transformar"),
        (59, [], "transformar"),
        (60, [], "donar"),
    ],
)
def test_reglas_5_a_7_sobremaduro_segun_manchas(manchas, defectos, tipo):
    assert recomendar_accion(lectura(manchas=manchas, defectos=defectos), "sobremaduro", MANGO)["tipo"] == tipo


def test_transformar_indica_el_destino_del_producto():
    accion = recomendar_accion(lectura(manchas=40), "sobremaduro", MANGO)
    assert "jugos o pulpa" in accion["mensaje"]


def test_donar_requiere_confirmacion_del_jefe():
    assert recomendar_accion(lectura(manchas=70), "sobremaduro", MANGO)["requiere_confirmacion"] is True
