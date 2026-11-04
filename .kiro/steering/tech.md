---
inclusion: always
---
# Tecnología

- **Lenguaje:** Python 3.12. Tipado con anotaciones; `from __future__ import annotations` en cada módulo.
- **Servicio:** AWS Lambda detrás de Amazon API Gateway (HTTP API). Handler: `frescura.handler.lambda_handler`.
- **Visión:** Amazon Bedrock con la API Converse y tool use. Modelo por defecto `us.amazon.nova-2-lite-v1:0`, configurable con la variable `MODELO_VISION`.
- **Datos:** catálogo y nutrición en JSON dentro del paquete (`app/frescura/datos/`); historial en DynamoDB.
- **Infraestructura:** AWS CDK en Python (`infra/`). Un stack por participante: `Frescura-<participante>`.
- **Pruebas:** pytest; Hypothesis para pruebas basadas en propiedades. Las pruebas **nunca** llaman a AWS: usan `VisionEjemplo` y `HistorialEnMemoria`.
- **Calidad:** `ruff check .` y `ruff format .`, línea de 120 caracteres.

## Comandos
- Pruebas: `pytest`
- Lint: `ruff check .`
- Evaluación: `python eval/evaluar.py`
- Sintetizar la infraestructura: `cd infra && cdk synth -c participante=<iniciales>`

## Cambios de umbrales
Cuando se cambie un umbral en `app/frescura/datos/catalogo.json`, además de `pytest` hay que correr `python eval/evaluar.py` y confirmar que el acierto de etapa sigue en 85% o más: un umbral mal calibrado puede pasar las pruebas y aun así bajar el acierto. (Esta regla nació como una memoria de Kiro en el Lab 5.)

## Errores de la API
Siempre `{"error": {"code": "CODIGO_EN_MAYUSCULAS", "message": "texto en español"}}`, con 400 para validación, 404 ruta inexistente, 413 imagen grande, 415 formato y 502 si falla la visión.
