"""Vista del cliente comprador (requisito 6 de la spec accion-en-tienda)."""

import hashlib
import json

from conftest import IMAGEN_JPEG, evento, imagen_b64
from frescura.handler import lambda_handler
from frescura.vision import VisionEjemplo

CAMPOS_CLIENTE = {"producto", "nombre", "etapa", "dias_hasta_optimo", "mensaje_cliente", "nutricion", "reconocido"}


def analizar(cuerpo_extra: dict) -> tuple[int, dict]:
    resp = lambda_handler(evento("POST", "/analisis", {"imagen_base64": imagen_b64(), **cuerpo_extra}))
    return resp["statusCode"], json.loads(resp["body"])


def con_lectura(dependencias, **lectura):
    huella = hashlib.sha256(IMAGEN_JPEG).hexdigest()
    dependencias["vision"] = VisionEjemplo({huella: lectura})


def test_el_cliente_solo_recibe_informacion_publica(dependencias):
    estado, datos = analizar({"vista": "cliente"})
    assert estado == 200
    assert set(datos) == CAMPOS_CLIENTE
    assert "accion" not in datos and "lectura" not in datos
    assert datos["reconocido"] is True


def test_confianza_baja_no_se_muestra_como_reconocido(dependencias):
    con_lectura(dependencias, producto="mango", indice_madurez=50, confianza=0.69)
    _, datos = analizar({"vista": "cliente"})
    assert datos["reconocido"] is False


def test_producto_desconocido_no_se_muestra_como_reconocido(dependencias):
    con_lectura(dependencias, producto="pitahaya", indice_madurez=50, confianza=0.95)
    _, datos = analizar({"vista": "cliente"})
    assert datos["reconocido"] is False
    assert datos["producto"] == "desconocido"


def test_sin_vista_responde_la_vista_del_personal(dependencias):
    _, datos = analizar({"tienda": "T-001"})
    assert "accion" in datos and "lectura" in datos
    assert dependencias["historial"].registros[0]["canal"] == "tienda"


def test_el_cliente_se_registra_en_su_canal_y_sin_tienda(dependencias):
    analizar({"vista": "cliente", "tienda": "T-001"})
    registro = dependencias["historial"].registros[0]
    assert registro["canal"] == "cliente"
    assert registro["tienda"] is None


def test_vista_invalida(dependencias):
    estado, datos = analizar({"vista": "gerencia"})
    assert estado == 400
    assert datos["error"]["code"] == "VISTA_INVALIDA"


def test_el_cliente_recibe_su_mensaje(dependencias):
    _, datos = analizar({"vista": "cliente"})
    assert datos["mensaje_cliente"].startswith("Tu banano")
