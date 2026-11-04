# Instrucciones para agentes: app/frescura

- Las funciones de reglas (`reglas.py`, `acciones.py`, `nutricion.py`) son **puras**: no llaman a AWS, no leen variables de entorno y no escriben registros.
- Todo cambio en una regla lleva una prueba en `tests/` que cubra el límite exacto del umbral.
- No cambies la firma de `analizar_foto` ni los nombres de los campos de la respuesta sin actualizar `web/index.html`, `web/cliente.html`, `app/frescura/vista_cliente.py` y sus pruebas. La vista del cliente nunca debe incluir `accion` ni `lectura`.
