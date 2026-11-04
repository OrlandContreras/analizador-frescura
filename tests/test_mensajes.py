"""Pruebas del mensaje para el cliente (Lab 8, construido por el agente implementador)."""

from datetime import date

import pytest

from frescura.mensajes import mensaje_cliente

LUNES = date(2026, 11, 2)
PALABRAS_PROHIBIDAS = ("cura", "previene", "sana", "adelgaza", "quema grasa", "desintoxica", "garantiza")


def test_pinton_dice_el_dia_de_la_semana():
    assert mensaje_cliente("Aguacate hass", "pinton", 3, LUNES) == (
        "Tu aguacate hass estará en su punto el jueves. Mientras tanto, déjalo a temperatura ambiente."
    )


def test_un_dia_dice_manana():
    assert "mañana" in mensaje_cliente("Mango", "pinton", 1, LUNES)


def test_cruza_el_fin_de_semana():
    assert "el domingo" in mensaje_cliente("Papaya", "verde", 6, LUNES)


def test_maduro_esta_en_su_punto():
    assert mensaje_cliente("Banano", "maduro", 0, LUNES) == "Tu banano está en su punto. Disfrútalo hoy o mañana."


def test_sobremaduro_sugiere_aprovecharlo_hoy():
    assert "Aprovéchalo hoy" in mensaje_cliente("Tomate chonto", "sobremaduro", 0, LUNES)


def test_producto_desconocido_no_tiene_mensaje():
    assert mensaje_cliente(None, None, None, LUNES) is None


@pytest.mark.parametrize("etapa,dias", [("verde", 5), ("pinton", 2), ("maduro", 0), ("sobremaduro", 0)])
def test_nunca_promete_efectos_de_salud_y_usa_maximo_dos_frases(etapa, dias):
    texto = mensaje_cliente("Mango", etapa, dias, LUNES)
    assert not any(palabra in texto.lower() for palabra in PALABRAS_PROHIBIDAS)
    assert texto.count(".") <= 2
