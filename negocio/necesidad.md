# Necesidad de negocio: menos pérdida en frutas y verduras

> **Documento ficticio para el workshop de Kiro.** Las cifras son de ejemplo y no corresponden a datos de Grupo Éxito.

## Situación actual

- En las tiendas del piloto, la sección de frutas y verduras pierde cerca del **8% de lo que recibe**. La mayor parte (unas **6 de cada 10 unidades perdidas**) se pierde por sobremaduración que se detecta tarde.
- La revisión es manual: el auxiliar de la sección recorre la góndola cada mañana, tarda unos **45 minutos** y decide a ojo qué rebajar, qué pasar a producción y qué retirar. Cada tienda decide distinto.
- No queda registro de esas decisiones, así que no se puede medir qué funcionó.

## Lo que necesitamos

Un analizador que, con una foto tomada desde el celular, le diga al personal de la sección:

1. Qué producto es y en qué **etapa de madurez** está (verde, pintón, maduro, sobremaduro).
2. **Cuántos días faltan** para su punto óptimo.
3. Qué **acción tomar en la tienda**, según la política POL-FRV-001 (`politica-acciones-tienda.md`).
4. Su **información nutricional por porción**, que más adelante verá el cliente en la app.

Cada análisis debe quedar registrado (sin guardar la foto) para medir el uso y el efecto en la pérdida.

## Usuarios

| Usuario | Fase | Qué hace con el analizador |
| --- | --- | --- |
| Auxiliar de frutas y verduras | Piloto | Fotografía los productos en la ronda de la mañana y aplica la acción recomendada |
| Jefe de sección | Piloto | Revisa los casos marcados "revisar" y confirma las donaciones |
| Cliente en la app de Éxito o Carulla | Fase siguiente | Consulta cuándo estará en su punto lo que compró y qué aporta por porción |

## Alcance del MVP del workshop

- 5 productos: banano, aguacate hass, tomate chonto, mango y papaya.
- Una foto por producto, tomada de cerca y con buena luz.
- Una instancia por participante en una cuenta de pruebas de AWS.

## Fuera de alcance por ahora

- Integración con inventario, precios o el sistema de rebajas.
- Análisis de una góndola completa en una sola foto.
- Recomendaciones de salud personalizadas para clientes.

## Cómo sabremos que funciona (indicadores del piloto)

| Indicador | Meta del piloto |
| --- | --- |
| Acierto de la etapa de madurez en fotos etiquetadas | 85% o más |
| Pérdida en frutas y verduras de las tiendas piloto | Bajar del 8% al 6,5% en 3 meses |
| Tiempo de la ronda de la mañana | Bajar de 45 a 25 minutos |
| Análisis marcados "revisar" | Menos del 15% |
