"""Catálogo de productos y tabla de nutrición, cargados desde los archivos JSON del paquete."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_DATOS = Path(__file__).parent / "datos"


@lru_cache(maxsize=1)
def cargar_catalogo() -> dict[str, dict]:
    """Devuelve los productos del catálogo indexados por id."""
    contenido = json.loads((_DATOS / "catalogo.json").read_text(encoding="utf-8"))
    return {producto["id"]: producto for producto in contenido["productos"]}


@lru_cache(maxsize=1)
def cargar_nutricion() -> dict:
    """Devuelve la tabla de nutrición completa (fuente y valores por 100 g)."""
    return json.loads((_DATOS / "nutricion.json").read_text(encoding="utf-8"))


def obtener_producto(producto_id: str) -> dict | None:
    return cargar_catalogo().get(producto_id)


def ids_productos() -> list[str]:
    return list(cargar_catalogo().keys())
