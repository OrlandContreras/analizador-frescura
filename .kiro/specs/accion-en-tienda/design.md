# Design Document

## Overview

Se agrega un módulo de reglas puro, `app/frescura/acciones.py`, con la función `recomendar_accion(lectura, etapa, producto)`. El servicio `analizar_foto` la llama después de calcular la etapa y agrega el resultado en el campo `accion` de la respuesta. Además, `app/frescura/vista_cliente.py` filtra la respuesta para la vista del cliente, y la API recibe el campo `vista`. No cambia la infraestructura ni el modelo de visión.

## Architecture

```
handler.lambda_handler ──► analizador.analizar_foto
                              ├─ vision.analizar          (lectura)
                              ├─ reglas.etapa_madurez      (etapa)
                              ├─ acciones.recomendar_accion (NUEVO)
                              └─ nutricion.nutricion_por_porcion
handler ──► vista_cliente.para_cliente   (NUEVO, solo si vista = "cliente")
handler ──► historial.guardar(..., canal) (canal "tienda" o "cliente")
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

### `vista_cliente.para_cliente(resultado: dict) -> dict`

Devuelve solo `producto`, `nombre`, `etapa`, `dias_hasta_optimo`, `nutricion` y `reconocido`. `reconocido` es falso si el producto es `desconocido` o si `lectura.confianza < UMBRAL_CONFIANZA` (el mismo umbral de `acciones.py`). Nunca copia `accion` ni `lectura`.

### API: campo `vista`

`POST /analisis` acepta `"vista": "tienda" | "cliente"` (por defecto `tienda`). Otro valor responde 400 `VISTA_INVALIDA`. Para el cliente, se ignora `tienda` y se registra el canal `cliente`.

## Data Models

```json
"accion": {"tipo": "transformar", "mensaje": "Enviar a jugos o pulpa", "requiere_confirmacion": false}
```

Respuesta para el cliente:

```json
{"producto": "mango", "nombre": "Mango", "etapa": "pinton", "dias_hasta_optimo": 2, "nutricion": {...}, "reconocido": true}
```

Historial: se agrega el atributo `canal` (`tienda` o `cliente`).

## Error Handling

`recomendar_accion` no lanza excepciones: cualquier lectura incompleta cae en la regla 1 (`revisar`).

## Testing Strategy

- `tests/test_acciones.py`: una prueba por regla, incluidos los límites exactos (confianza 0,70; manchas 29, 30, 59 y 60).
- `tests/test_handler.py`: la respuesta del análisis incluye `accion`.
- `tests/test_vista_cliente.py`: la vista del cliente no incluye `accion` ni `lectura`, marca `reconocido` y la API rechaza una `vista` inválida.
- Las pruebas no llaman a AWS.
