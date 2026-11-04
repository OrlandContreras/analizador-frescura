"""Visión: describe la foto (producto, índice de madurez, manchas, defectos y confianza).

Hay dos implementaciones con la misma interfaz:
- VisionBedrock: llama a un modelo multimodal de Amazon Bedrock con la API Converse.
- VisionEjemplo: devuelve lecturas fijas. Se usa en las pruebas y en la evaluación sin costo.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from typing import Protocol

from .catalogo import cargar_catalogo

DEFECTOS_VALIDOS = ("moho", "golpes", "cortes", "zonas_hundidas")
MODELO_POR_DEFECTO = "us.amazon.nova-2-lite-v1:0"


@dataclass
class LecturaVision:
    producto: str
    indice_madurez: float
    manchas_pct: float
    defectos: list[str] = field(default_factory=list)
    confianza: float = 0.0

    def a_dict(self) -> dict:
        return asdict(self)


class Vision(Protocol):
    def analizar(self, imagen: bytes, formato: str) -> LecturaVision: ...


def normalizar_lectura(datos: dict) -> LecturaVision:
    """Convierte la respuesta del modelo en una lectura válida.

    Lo que el modelo no pueda justificar queda con confianza 0, para que las reglas
    lo manden a revisión humana en lugar de recomendar una acción.
    """
    catalogo = cargar_catalogo()
    producto = str(datos.get("producto", "desconocido")).strip().lower()
    confianza = _acotar(datos.get("confianza"), 0.0, 1.0, por_defecto=0.0)
    if producto not in catalogo:
        producto = "desconocido"
        confianza = 0.0
    defectos = [d for d in datos.get("defectos", []) if d in DEFECTOS_VALIDOS]
    return LecturaVision(
        producto=producto,
        indice_madurez=_acotar(datos.get("indice_madurez"), 0.0, 100.0, por_defecto=0.0),
        manchas_pct=_acotar(datos.get("manchas_pct"), 0.0, 100.0, por_defecto=0.0),
        defectos=defectos,
        confianza=confianza,
    )


def _acotar(valor, minimo: float, maximo: float, por_defecto: float) -> float:
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return por_defecto
    if numero != numero:  # NaN
        return por_defecto
    return max(minimo, min(maximo, numero))


def _instrucciones() -> str:
    lineas = [
        "Eres un inspector de calidad de frutas y verduras de un supermercado en Colombia.",
        "Analiza la foto y registra tu lectura con la herramienta registrar_lectura.",
        "Productos posibles y su escala de madurez (indice_madurez de 0 a 100):",
    ]
    for producto in cargar_catalogo().values():
        lineas.append(f"- {producto['id']} ({producto['nombre']}): {producto['escala_visual']}")
    lineas += [
        "Si la foto no muestra con claridad uno de estos productos, usa producto = desconocido y confianza 0.",
        "manchas_pct es el porcentaje aproximado de la superficie visible con manchas.",
        "confianza va de 0 a 1 y refleja qué tan seguro estás del producto y del índice.",
    ]
    return "\n".join(lineas)


def _herramienta() -> dict:
    return {
        "toolSpec": {
            "name": "registrar_lectura",
            "description": "Registra la lectura visual de una fruta o verdura.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "producto": {"type": "string", "enum": [*cargar_catalogo().keys(), "desconocido"]},
                        "indice_madurez": {"type": "number", "minimum": 0, "maximum": 100},
                        "manchas_pct": {"type": "number", "minimum": 0, "maximum": 100},
                        "defectos": {"type": "array", "items": {"type": "string", "enum": list(DEFECTOS_VALIDOS)}},
                        "confianza": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                    "required": ["producto", "indice_madurez", "manchas_pct", "defectos", "confianza"],
                }
            },
        }
    }


class VisionBedrock:
    """Lectura con un modelo multimodal de Amazon Bedrock (API Converse + tool use)."""

    def __init__(self, cliente=None, modelo: str | None = None):
        if cliente is None:
            import boto3

            cliente = boto3.client("bedrock-runtime")
        self._cliente = cliente
        self._modelo = modelo or os.environ.get("MODELO_VISION", MODELO_POR_DEFECTO)

    def analizar(self, imagen: bytes, formato: str) -> LecturaVision:
        respuesta = self._cliente.converse(
            modelId=self._modelo,
            system=[{"text": _instrucciones()}],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"image": {"format": formato, "source": {"bytes": imagen}}},
                        {"text": "Registra la lectura de este producto."},
                    ],
                }
            ],
            toolConfig={"tools": [_herramienta()], "toolChoice": {"tool": {"name": "registrar_lectura"}}},
            inferenceConfig={"maxTokens": 400, "temperature": 0},
        )
        return normalizar_lectura(_extraer_datos(respuesta))


def _extraer_datos(respuesta: dict) -> dict:
    """Toma la llamada a la herramienta; si no la hay, intenta leer un JSON del texto."""
    contenido = respuesta.get("output", {}).get("message", {}).get("content", [])
    for bloque in contenido:
        if "toolUse" in bloque:
            return bloque["toolUse"].get("input", {})
    for bloque in contenido:
        texto = bloque.get("text", "")
        inicio, fin = texto.find("{"), texto.rfind("}")
        if inicio != -1 and fin > inicio:
            try:
                return json.loads(texto[inicio : fin + 1])
            except json.JSONDecodeError:
                pass
    return {}


class VisionEjemplo:
    """Devuelve lecturas fijas, buscadas por la huella SHA-256 de la imagen.

    Si la imagen no está registrada, devuelve la lectura por defecto.
    """

    def __init__(self, lecturas: dict[str, dict] | None = None, por_defecto: dict | None = None):
        self._lecturas = lecturas or {}
        self._por_defecto = por_defecto or {
            "producto": "banano",
            "indice_madurez": 60,
            "manchas_pct": 5,
            "defectos": [],
            "confianza": 0.9,
        }

    def analizar(self, imagen: bytes, formato: str) -> LecturaVision:
        huella = hashlib.sha256(imagen).hexdigest()
        return normalizar_lectura(self._lecturas.get(huella, self._por_defecto))
