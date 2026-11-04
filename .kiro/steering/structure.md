---
inclusion: always
---
# Estructura del proyecto

```
app/frescura/        Código de la función Lambda
  handler.py         Rutas, validación de entrada y respuestas HTTP
  analizador.py      Orquesta visión, reglas, acción y nutrición
  vision.py          Lectura con Bedrock (VisionBedrock) o fija (VisionEjemplo)
  reglas.py          Etapa de madurez y días hasta el punto óptimo
  acciones.py        Acción en tienda según POL-FRV-001
  nutricion.py       Nutrición por porción
  historial.py       Historial en DynamoDB (sin imágenes)
  datos/             catalogo.json y nutricion.json
infra/               AWS CDK: app.py y stacks/frescura_stack.py
web/                 Página web móvil (un solo index.html)
tests/               Pruebas de pytest, una por módulo
eval/                Evaluación del acierto con fotos etiquetadas
negocio/             Necesidad, política y glosario
laboratorios/        Guías del workshop (no forman parte del producto)
```

- Una regla de negocio nueva va en su propio módulo puro, sin llamadas a AWS, con su archivo de pruebas.
- El handler solo valida, llama a `analizar_foto` y arma la respuesta.
