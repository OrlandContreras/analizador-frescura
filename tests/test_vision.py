from frescura.vision import VisionBedrock, _extraer_datos, normalizar_lectura


def test_normaliza_valores_fuera_de_rango():
    lectura = normalizar_lectura(
        {"producto": "Mango", "indice_madurez": 140, "manchas_pct": -3, "defectos": ["moho", "otro"], "confianza": 2}
    )
    assert lectura.producto == "mango"
    assert lectura.indice_madurez == 100
    assert lectura.manchas_pct == 0
    assert lectura.defectos == ["moho"]
    assert lectura.confianza == 1


def test_producto_fuera_del_catalogo_queda_desconocido_y_sin_confianza():
    lectura = normalizar_lectura({"producto": "pitahaya", "indice_madurez": 50, "confianza": 0.9})
    assert lectura.producto == "desconocido"
    assert lectura.confianza == 0


def test_extrae_la_llamada_a_la_herramienta():
    respuesta = {"output": {"message": {"content": [{"toolUse": {"input": {"producto": "papaya"}}}]}}}
    assert _extraer_datos(respuesta) == {"producto": "papaya"}


def test_si_no_hay_herramienta_lee_json_del_texto():
    respuesta = {"output": {"message": {"content": [{"text": 'Lectura: {"producto": "tomate_chonto"}'}]}}}
    assert _extraer_datos(respuesta) == {"producto": "tomate_chonto"}


class ClienteFalso:
    def __init__(self):
        self.llamada = None

    def converse(self, **kwargs):
        self.llamada = kwargs
        return {
            "output": {
                "message": {
                    "content": [
                        {
                            "toolUse": {
                                "input": {
                                    "producto": "banano",
                                    "indice_madurez": 55,
                                    "manchas_pct": 10,
                                    "defectos": [],
                                    "confianza": 0.92,
                                }
                            }
                        }
                    ]
                }
            }
        }


def test_vision_bedrock_envia_la_imagen_y_obliga_la_herramienta():
    cliente = ClienteFalso()
    lectura = VisionBedrock(cliente=cliente, modelo="modelo-de-prueba").analizar(b"\xff\xd8\xffabc", "jpeg")

    assert lectura.producto == "banano"
    assert cliente.llamada["modelId"] == "modelo-de-prueba"
    imagen = cliente.llamada["messages"][0]["content"][0]["image"]
    assert imagen == {"format": "jpeg", "source": {"bytes": b"\xff\xd8\xffabc"}}
    assert cliente.llamada["toolConfig"]["toolChoice"] == {"tool": {"name": "registrar_lectura"}}
