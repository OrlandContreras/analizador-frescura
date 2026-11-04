"""Historial de análisis en Amazon DynamoDB. Nunca guarda la imagen."""

from __future__ import annotations

import os
import uuid
from datetime import UTC, datetime
from decimal import Decimal


class HistorialDynamo:
    def __init__(self, tabla=None, nombre_tabla: str | None = None):
        if tabla is None:
            import boto3

            tabla = boto3.resource("dynamodb").Table(nombre_tabla or os.environ["TABLA_ANALISIS"])
        self._tabla = tabla

    def guardar(self, resultado: dict, tienda: str | None) -> str:
        id_analisis = str(uuid.uuid4())
        lectura = resultado["lectura"]
        self._tabla.put_item(
            Item={
                "id": id_analisis,
                "fecha": datetime.now(UTC).isoformat(),
                "tienda": tienda or "sin-tienda",
                "producto": resultado["producto"],
                "etapa": resultado["etapa"] or "sin-etapa",
                "indice_madurez": Decimal(str(lectura["indice_madurez"])),
                "confianza": Decimal(str(lectura["confianza"])),
            }
        )
        return id_analisis


class HistorialEnMemoria:
    """Para pruebas y ejecución local."""

    def __init__(self):
        self.registros: list[dict] = []

    def guardar(self, resultado: dict, tienda: str | None) -> str:
        id_analisis = f"local-{len(self.registros) + 1}"
        self.registros.append({"id": id_analisis, "tienda": tienda, **resultado})
        return id_analisis
