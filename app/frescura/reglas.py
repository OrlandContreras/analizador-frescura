"""Reglas de madurez: deciden la etapa con los umbrales del catálogo.

El modelo de visión solo describe lo que ve (producto e índice de madurez de 0 a 100).
La decisión la toman estas reglas, que define el negocio y se pueden probar.
"""

from __future__ import annotations

import math

ETAPAS = ("verde", "pinton", "maduro", "sobremaduro")


def etapa_madurez(indice: float, umbrales: dict) -> str:
    """Devuelve la etapa de madurez para un índice de 0 a 100.

    Cada umbral marca el inicio de su etapa: un índice igual al umbral ya pertenece
    a esa etapa.
    """
    if indice > umbrales["sobremaduro"]:
        return "sobremaduro"
    if indice >= umbrales["maduro"]:
        return "maduro"
    if indice >= umbrales["pinton"]:
        return "pinton"
    return "verde"


def dias_hasta_optimo(indice: float, umbrales: dict, velocidad_dia: float) -> int:
    """Días que faltan para que el producto llegue a la etapa madura.

    Devuelve 0 si ya está maduro o sobremaduro.
    """
    faltante = umbrales["maduro"] - indice
    if faltante <= 0:
        return 0
    return math.ceil(faltante / velocidad_dia)
