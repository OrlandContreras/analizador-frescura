"""Función AWS Lambda detrás de Amazon API Gateway (HTTP API, payload 2.0).

Rutas:
- GET  /salud      Comprueba que la API responde.
- GET  /productos  Lista los productos que reconoce el analizador.
- POST /analisis   Analiza una foto. Cuerpo JSON: {"imagen_base64": "...", "gramos": 150, "tienda": "T-001"}
"""

from __future__ import annotations

import base64
import binascii
import json
import logging

from .analizador import analizar_foto
from .catalogo import cargar_catalogo

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TAMANO_MAXIMO_BYTES = 4 * 1024 * 1024
_dependencias: dict = {}


def obtener_dependencias() -> dict:
    """Crea una sola vez la visión y el historial (se reutilizan entre invocaciones)."""
    if not _dependencias:
        from .historial import HistorialDynamo
        from .vision import VisionBedrock

        _dependencias["vision"] = VisionBedrock()
        _dependencias["historial"] = HistorialDynamo()
    return _dependencias


def respuesta(status: int, cuerpo: dict) -> dict:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "body": json.dumps(cuerpo, ensure_ascii=False),
    }


def error(status: int, codigo: str, mensaje: str) -> dict:
    return respuesta(status, {"error": {"code": codigo, "message": mensaje}})


def detectar_formato(imagen: bytes) -> str | None:
    if imagen.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if imagen.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    return None


def lambda_handler(event: dict, context=None) -> dict:
    metodo = event.get("requestContext", {}).get("http", {}).get("method", "")
    ruta = event.get("rawPath", "")

    if metodo == "GET" and ruta == "/salud":
        return respuesta(200, {"estado": "ok"})
    if metodo == "GET" and ruta == "/productos":
        productos = [{"id": p["id"], "nombre": p["nombre"]} for p in cargar_catalogo().values()]
        return respuesta(200, {"productos": productos})
    if metodo == "POST" and ruta == "/analisis":
        return _analizar(event)
    return error(404, "NO_ENCONTRADO", "Ruta no encontrada")


def _analizar(event: dict) -> dict:
    cuerpo_texto = event.get("body") or ""
    if event.get("isBase64Encoded"):
        cuerpo_texto = base64.b64decode(cuerpo_texto).decode("utf-8")
    try:
        cuerpo = json.loads(cuerpo_texto)
    except json.JSONDecodeError:
        return error(400, "JSON_INVALIDO", "El cuerpo debe ser JSON")
    if not isinstance(cuerpo, dict):
        return error(400, "JSON_INVALIDO", "El cuerpo debe ser un objeto JSON")

    imagen_b64 = cuerpo.get("imagen_base64")
    if not isinstance(imagen_b64, str) or not imagen_b64:
        return error(400, "IMAGEN_REQUERIDA", "Falta imagen_base64")
    if "," in imagen_b64[:100] and imagen_b64.startswith("data:"):
        imagen_b64 = imagen_b64.split(",", 1)[1]
    try:
        imagen = base64.b64decode(imagen_b64, validate=True)
    except (binascii.Error, ValueError):
        return error(400, "IMAGEN_INVALIDA", "imagen_base64 no es base64 válido")
    if len(imagen) > TAMANO_MAXIMO_BYTES:
        return error(413, "IMAGEN_MUY_GRANDE", "La imagen supera 4 MB")
    formato = detectar_formato(imagen)
    if formato is None:
        return error(415, "FORMATO_NO_SOPORTADO", "Solo se aceptan imágenes JPEG o PNG")

    gramos = cuerpo.get("gramos", 100)
    if isinstance(gramos, bool) or not isinstance(gramos, (int, float)) or not 1 <= gramos <= 2000:
        return error(400, "GRAMOS_INVALIDOS", "gramos debe ser un número entre 1 y 2000")
    tienda = cuerpo.get("tienda")
    if tienda is not None and (not isinstance(tienda, str) or len(tienda) > 40):
        return error(400, "TIENDA_INVALIDA", "tienda debe ser un texto de hasta 40 caracteres")

    deps = obtener_dependencias()
    try:
        resultado = analizar_foto(deps["vision"], imagen, formato, gramos)
    except Exception:  # noqa: BLE001 - se registra y se responde sin exponer detalles
        logger.exception("Falló el análisis de la imagen")
        return error(502, "VISION_NO_DISPONIBLE", "No se pudo analizar la imagen. Intenta de nuevo")

    resultado["id"] = deps["historial"].guardar(resultado, tienda)
    logger.info(
        json.dumps(
            {"evento": "analisis", "producto": resultado["producto"], "etapa": resultado["etapa"], "tienda": tienda}
        )
    )
    return respuesta(200, resultado)
