import base64
import hashlib
import json

from conftest import IMAGEN_JPEG, evento, imagen_b64
from frescura.handler import lambda_handler
from frescura.vision import VisionEjemplo


def cuerpo(resp):
    return json.loads(resp["body"])


def test_salud(dependencias):
    resp = lambda_handler(evento("GET", "/salud"))
    assert resp["statusCode"] == 200


def test_lista_los_cinco_productos(dependencias):
    resp = lambda_handler(evento("GET", "/productos"))
    assert len(cuerpo(resp)["productos"]) == 5


def test_analiza_una_foto_y_guarda_el_historial(dependencias):
    resp = lambda_handler(
        evento("POST", "/analisis", {"imagen_base64": imagen_b64(), "gramos": 120, "tienda": "T-001"})
    )

    assert resp["statusCode"] == 200
    datos = cuerpo(resp)
    assert datos["producto"] == "banano"
    assert datos["etapa"] == "maduro"
    assert datos["nutricion"]["gramos"] == 120
    assert datos["accion"]["tipo"] == "priorizar"
    assert datos["mensaje_cliente"] == "Tu banano está en su punto. Disfrútalo hoy o mañana."
    assert datos["id"] == "local-1"
    assert dependencias["historial"].registros[0]["tienda"] == "T-001"


def test_acepta_data_url_de_la_web(dependencias):
    data_url = "data:image/jpeg;base64," + imagen_b64()
    resp = lambda_handler(evento("POST", "/analisis", {"imagen_base64": data_url}))
    assert resp["statusCode"] == 200


def test_acepta_cuerpo_en_base64(dependencias):
    ev = evento("POST", "/analisis", {"imagen_base64": imagen_b64()})
    ev["body"] = base64.b64encode(ev["body"].encode()).decode()
    ev["isBase64Encoded"] = True
    assert lambda_handler(ev)["statusCode"] == 200


def test_producto_desconocido_no_tiene_etapa(dependencias):
    huella = hashlib.sha256(IMAGEN_JPEG).hexdigest()
    dependencias["vision"] = VisionEjemplo({huella: {"producto": "pitahaya", "indice_madurez": 50, "confianza": 0.9}})
    datos = cuerpo(lambda_handler(evento("POST", "/analisis", {"imagen_base64": imagen_b64()})))
    assert datos["producto"] == "desconocido"
    assert datos["etapa"] is None
    assert datos["accion"]["tipo"] == "revisar"
    assert datos["mensaje_cliente"] is None


def test_errores_de_validacion(dependencias):
    casos = [
        ({}, 400, "IMAGEN_REQUERIDA"),
        ({"imagen_base64": "%%%"}, 400, "IMAGEN_INVALIDA"),
        ({"imagen_base64": imagen_b64(b"GIF89a")}, 415, "FORMATO_NO_SOPORTADO"),
        ({"imagen_base64": imagen_b64(), "gramos": 0}, 400, "GRAMOS_INVALIDOS"),
        ({"imagen_base64": imagen_b64(), "gramos": True}, 400, "GRAMOS_INVALIDOS"),
    ]
    for datos, status, codigo in casos:
        resp = lambda_handler(evento("POST", "/analisis", datos))
        assert resp["statusCode"] == status, codigo
        assert cuerpo(resp)["error"]["code"] == codigo


def test_imagen_muy_grande(dependencias):
    grande = b"\xff\xd8\xff" + b"0" * (4 * 1024 * 1024)
    resp = lambda_handler(evento("POST", "/analisis", {"imagen_base64": imagen_b64(grande)}))
    assert resp["statusCode"] == 413


def test_falla_de_la_vision_responde_502(dependencias):
    class VisionCaida:
        def analizar(self, imagen, formato):
            raise RuntimeError("Bedrock no disponible")

    dependencias["vision"] = VisionCaida()
    resp = lambda_handler(evento("POST", "/analisis", {"imagen_base64": imagen_b64()}))
    assert resp["statusCode"] == 502
    assert "Bedrock" not in resp["body"]


def test_ruta_inexistente(dependencias):
    assert lambda_handler(evento("GET", "/nada"))["statusCode"] == 404
