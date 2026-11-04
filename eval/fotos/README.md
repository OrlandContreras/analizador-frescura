# Fotos de evaluación

Aquí van las 60 fotos que nombra `eval/etiquetas.csv` (por ejemplo `banano_verde_1.jpg`): 3 por cada producto y etapa.

- Para el piloto, las toma el equipo de la tienda con frutas y verduras reales. Las fotos de una colección pública no sirven para medir el acierto: tienen otra luz, otro fondo y otras variedades.
- En el taller no hacen falta: la evaluación usa las lecturas de ejemplo, y para probar la instancia desplegada están las fotos de muestra de `web/muestras/`.
- Un solo producto por foto, de cerca, con luz de día y fondo neutro. Sin personas ni marcas en la imagen.
- La etapa de cada foto la confirma una persona del área de frutas y verduras antes de usarla.

Con las fotos en esta carpeta se puede correr `python eval/evaluar.py --modo bedrock`. Sin ellas, `python eval/evaluar.py` usa las lecturas de ejemplo de `eval/lecturas_ejemplo.json`.
