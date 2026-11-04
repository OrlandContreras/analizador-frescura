---
inclusion: manual
---
# Guía de diagnóstico

Úsala escribiendo `#troubleshooting` en el chat.

1. Antes de cambiar código, reproduce el problema con una prueba que falle.
2. Si `pytest` no encuentra `frescura`, corre los comandos desde la raíz del proyecto, con el entorno virtual activado.
3. Si una prueba intenta llamar a AWS, reemplaza la dependencia con `VisionEjemplo` o `HistorialEnMemoria` (ver `tests/conftest.py`).
4. Si `cdk synth` falla con "Falta tu identificador", agrega `-c participante=<iniciales>`.
5. Si la API responde 502 `VISION_NO_DISPONIBLE`, revisa en CloudWatch los registros de la función: suele ser acceso al modelo de Bedrock no habilitado o un límite de llamadas.
