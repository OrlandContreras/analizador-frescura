"""Información nutricional por porción."""

from __future__ import annotations

from .catalogo import cargar_nutricion

GRAMOS_POR_DEFECTO = 100


def nutricion_por_porcion(producto_id: str, gramos: float = GRAMOS_POR_DEFECTO) -> dict | None:
    """Escala los valores por 100 g a la porción pedida. Devuelve None si no hay datos."""
    tabla = cargar_nutricion()
    base = tabla["por_100g"].get(producto_id)
    if base is None:
        return None
    factor = gramos / 100
    return {
        "gramos": gramos,
        "energia_kcal": round(base["energia_kcal"] * factor, 1),
        "fibra_g": round(base["fibra_g"] * factor, 1),
        "potasio_mg": round(base["potasio_mg"] * factor, 1),
        "vitamina_c_mg": round(base["vitamina_c_mg"] * factor, 1),
        "fuente": tabla["fuente"],
        "aviso": "Valores aproximados de referencia. No reemplazan la orientación de un profesional de la salud.",
    }
