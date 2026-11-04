"""Vista del cliente comprador: solo información pública del producto (POL-FRV-001, sección 6)."""

from __future__ import annotations

from .acciones import UMBRAL_CONFIANZA

CAMPOS_PUBLICOS = ("producto", "nombre", "etapa", "dias_hasta_optimo", "nutricion")


def para_cliente(resultado: dict) -> dict:
    """Filtra el resultado del análisis: nunca incluye la acción en tienda ni la lectura del modelo."""
    confianza = (resultado.get("lectura") or {}).get("confianza", 0)
    vista = {campo: resultado.get(campo) for campo in CAMPOS_PUBLICOS}
    vista["reconocido"] = resultado.get("producto") != "desconocido" and confianza >= UMBRAL_CONFIANZA
    return vista
