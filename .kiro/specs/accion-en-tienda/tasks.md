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

- [ ] 5. Crear la vista del cliente
  - Crear `app/frescura/vista_cliente.py` con `para_cliente(resultado)`
  - _Requirements: 6.1, 6.2, 6.3_

- [ ] 6. Aceptar la vista en la API y registrar el canal
  - En `app/frescura/handler.py`, validar `vista` y responder `para_cliente` cuando es `cliente`
  - En `app/frescura/historial.py`, agregar el parámetro `canal` y guardarlo; para el cliente, sin tienda
  - _Requirements: 6.4, 6.5, 6.6_

- [ ] 7. Probar la vista del cliente
  - Crear `tests/test_vista_cliente.py`: sin `accion` ni `lectura`, `reconocido` falso con confianza 0,69 y producto desconocido, error 400 con una vista inválida y canal registrado
  - _Requirements: 6.1–6.6_

- [ ] 8. Verificar
  - Correr `pytest` y `ruff check .`; todo debe pasar
