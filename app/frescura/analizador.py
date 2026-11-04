"""Servicio del analizador: combina la lectura de visión, las reglas y la nutrición."""

from __future__ import annotations

from .catalogo import obtener_producto
from .nutricion import GRAMOS_POR_DEFECTO, nutricion_por_porcion
from .reglas import dias_hasta_optimo, etapa_madurez
from .vision import Vision


def analizar_foto(vision: Vision, imagen: bytes, formato: str, gramos: float = GRAMOS_POR_DEFECTO) -> dict:
    """Analiza una foto y devuelve el resultado completo para la API."""
    lectura = vision.analizar(imagen, formato)
    producto = obtener_producto(lectura.producto)
    if producto is None:
        return {
            "producto": "desconocido",
            "nombre": None,
            "etapa": None,
            "dias_hasta_optimo": None,
            "nutricion": None,
            "lectura": lectura.a_dict(),
        }
    return {
        "producto": producto["id"],
        "nombre": producto["nombre"],
        "etapa": etapa_madurez(lectura.indice_madurez, producto["umbrales"]),
        "dias_hasta_optimo": dias_hasta_optimo(
            lectura.indice_madurez, producto["umbrales"], producto["velocidad_maduracion_dia"]
        ),
        "nutricion": nutricion_por_porcion(producto["id"], gramos),
        "lectura": lectura.a_dict(),
    }
