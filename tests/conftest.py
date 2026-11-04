import base64

import pytest

from frescura import handler
from frescura.historial import HistorialEnMemoria
from frescura.vision import VisionEjemplo

# Bytes que empiezan como un JPEG. Las pruebas no decodifican la imagen: la visión es de ejemplo.
IMAGEN_JPEG = b"\xff\xd8\xff\xe0" + b"foto-de-prueba"


@pytest.fixture
def dependencias(monkeypatch):
    """Reemplaza Bedrock y DynamoDB por dobles en memoria."""
    deps = {"vision": VisionEjemplo(), "historial": HistorialEnMemoria()}
    monkeypatch.setattr(handler, "_dependencias", deps)
    return deps


def evento(metodo: str, ruta: str, cuerpo: dict | None = None) -> dict:
    import json

    return {
        "rawPath": ruta,
        "requestContext": {"http": {"method": metodo}},
        "body": json.dumps(cuerpo) if cuerpo is not None else None,
        "isBase64Encoded": False,
    }


def imagen_b64(imagen: bytes = IMAGEN_JPEG) -> str:
    return base64.b64encode(imagen).decode()
