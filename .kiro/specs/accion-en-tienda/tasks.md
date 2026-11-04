# Implementation Plan

- [ ] 1. Crear el módulo de acciones
  - Crear `app/frescura/acciones.py` con las constantes y `recomendar_accion`
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1–3.6, 4.1–4.3_

- [ ] 2. Probar las reglas
  - Crear `tests/test_acciones.py` con una prueba por regla y por cada límite (0,70; 29, 30, 59 y 60)
  - _Requirements: 1.1, 2.1, 3.1–3.5_

- [ ] 3. Integrar la acción en el análisis
  - En `app/frescura/analizador.py`, agregar el campo `accion` en ambas respuestas (producto reconocido y desconocido)
  - _Requirements: 5.1, 5.2_

- [ ] 4. Probar la respuesta de la API
  - En `tests/test_handler.py`, comprobar que el análisis incluye `accion` y que un producto desconocido devuelve `revisar`
  - _Requirements: 5.1, 1.2_

- [ ] 5. Verificar
  - Correr `pytest` y `ruff check .`; todo debe pasar
