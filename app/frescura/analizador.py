"""Servicio del analizador: combina visión, reglas, acción en tienda, mensaje al cliente y nutrición."""

from __future__ import annotations

from datetime import date

from .acciones import recomendar_accion
from .catalogo import obtener_producto
from .mensajes import mensaje_cliente
from .nutricion import GRAMOS_POR_DEFECTO, nutricion_por_porcion
from .reglas import dias_hasta_optimo, etapa_madurez
from .vision import Vision


def analizar_foto(
    vision: Vision, imagen: bytes, formato: str, gramos: float = GRAMOS_POR_DEFECTO, hoy: date | None = None
) -> dict:
    """Analiza una foto y devuelve el resultado completo para la API."""
    lectura = vision.analizar(imagen, formato)
    producto = obtener_producto(lectura.producto)
    if producto is None:
        return {
            "producto": "desconocido",
            "nombre": None,
            "etapa": None,
            "dias_hasta_optimo": None,
            "accion": recomendar_accion(lectura, None, None),
            "mensaje_cliente": None,
            "nutricion": None,
            "lectura": lectura.a_dict(),
        }
    etapa = etapa_madurez(lectura.indice_madurez, producto["umbrales"])
    dias = dias_hasta_optimo(lectura.indice_madurez, producto["umbrales"], producto["velocidad_maduracion_dia"])
    return {
        "producto": producto["id"],
        "nombre": producto["nombre"],
        "etapa": etapa,
        "dias_hasta_optimo": dias,
        "accion": recomendar_accion(lectura, etapa, producto),
        "mensaje_cliente": mensaje_cliente(producto["nombre"], etapa, dias, hoy),
        "nutricion": nutricion_por_porcion(producto["id"], gramos),
        "lectura": lectura.a_dict(),
    }
