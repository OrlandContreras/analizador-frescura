# Design Document

## Overview

Se agrega un módulo de reglas puro, `app/frescura/acciones.py`, con la función `recomendar_accion(lectura, etapa, producto)`. El servicio `analizar_foto` la llama después de calcular la etapa y agrega el resultado en el campo `accion` de la respuesta. No cambia la infraestructura ni el modelo de visión.

## Architecture

```
handler.lambda_handler ──► analizador.analizar_foto
                              ├─ vision.analizar          (lectura)
                              ├─ reglas.etapa_madurez      (etapa)
                              ├─ acciones.recomendar_accion (NUEVO)
                              └─ nutricion.nutricion_por_porcion
```

## Components and Interfaces

### `acciones.recomendar_accion(lectura: LecturaVision, etapa: str | None, producto: dict | None) -> dict`

Evalúa las reglas en el orden de la política y devuelve la primera que se cumple:

| Orden | Condición | Acción | Requiere confirmación |
| --- | --- | --- | --- |
| 1 | producto o etapa ausentes, o confianza < 0,70 | `revisar` | Sí |
| 2 | `moho` en defectos | `retirar` | No |
| 3 | etapa verde o pinton | `mantener` | No |
| 4 | etapa maduro | `priorizar` | No |
| 5 | sobremaduro y manchas ≥ 60 | `donar` | Sí |
| 6 | sobremaduro y (manchas ≥ 30 o zonas_hundidas) | `transformar` | No |
| 7 | sobremaduro (resto) | `rebajar` | No |

Las reglas 5 a 7 se evalúan de mayor a menor gravedad, lo que es equivalente a la política.

Constantes: `UMBRAL_CONFIANZA = 0.70`, `MANCHAS_TRANSFORMAR = 30`, `MANCHAS_DONAR = 60`.

## Data Models

```json
"accion": {"tipo": "transformar", "mensaje": "Enviar a jugos o pulpa", "requiere_confirmacion": false}
```

## Error Handling

`recomendar_accion` no lanza excepciones: cualquier lectura incompleta cae en la regla 1 (`revisar`).

## Testing Strategy

- `tests/test_acciones.py`: una prueba por regla, incluidos los límites exactos (confianza 0,70; manchas 29, 30, 59 y 60).
- `tests/test_handler.py`: la respuesta del análisis incluye `accion`.
- Las pruebas no llaman a AWS.
