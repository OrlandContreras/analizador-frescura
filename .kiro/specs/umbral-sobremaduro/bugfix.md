# Bugfix: un producto justo en el umbral de sobremaduro sale como maduro

## Current Behavior

WHEN el índice de madurez es exactamente igual al umbral `sobremaduro` del producto (por ejemplo 80 para el banano), THE Analizador SHALL clasificarlo como `maduro`.

Evidencia:
- `tests/test_reglas.py::test_umbral_exacto_de_sobremaduro_ya_es_sobremaduro` falla: espera `sobremaduro` y recibe `maduro`.
- `python eval/evaluar.py` da 83,3% de acierto de etapa (mínimo 85%). Tres fotos sobremaduras con índice en el umbral exacto salen como maduras.
- Causa: en `app/frescura/reglas.py`, `etapa_madurez` compara `indice > umbrales["sobremaduro"]`, mientras los demás umbrales usan `>=`.

## Expected Behavior

WHEN el índice de madurez es igual o mayor al umbral `sobremaduro`, THE Analizador SHALL clasificarlo como `sobremaduro`, como dice el glosario: "un índice igual al umbral ya pertenece a esa etapa".

## Unchanged Behavior

- Los índices por debajo del umbral `sobremaduro` mantienen su etapa actual.
- Los umbrales `pinton` y `maduro` no cambian.
- El cálculo de días hasta el punto óptimo no cambia.
- Todas las pruebas que hoy pasan siguen pasando.
