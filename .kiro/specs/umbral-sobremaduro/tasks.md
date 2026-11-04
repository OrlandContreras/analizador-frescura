# Implementation Plan

- [ ] 1. Corregir la comparación del umbral de sobremaduro
  - En `app/frescura/reglas.py`, cambiar `indice > umbrales["sobremaduro"]` por `indice >= umbrales["sobremaduro"]`

- [ ] 2. Verificar
  - `pytest`: la prueba `test_umbral_exacto_de_sobremaduro_ya_es_sobremaduro` pasa y ninguna otra se rompe
  - `python eval/evaluar.py`: el acierto de etapa sube a 88,3% y cumple el mínimo de 85%
