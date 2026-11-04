---
name: estimar-costo-piloto
description: Estima el costo mensual en AWS de llevar el analizador de frescura a un piloto en tiendas, con precios reales consultados en el servidor MCP aws-pricing. Úsalo cuando pidan costo, presupuesto o estimación del piloto o de la solución.
---
# Estimación de costo del piloto

## Supuestos (pregúntalos si la persona no los da)
- Tiendas del piloto: 5
- Fotos por tienda y día: 200
- Días al mes: 30
- Región: us-east-1

## Procedimiento
1. Lee `infra/stacks/frescura_stack.py` y lista los servicios que usa la solución.
2. Para cada servicio, consulta el precio vigente **con el servidor MCP `aws-pricing`**. No uses precios de memoria. Si un precio no aparece, escribe "no disponible" y explica qué faltó.
3. Para Bedrock, estima por foto los tokens de entrada (imagen de 1024 px más las instrucciones) y de salida (unos 150 tokens), y explica el supuesto.
4. Calcula el costo mensual por servicio y el total, mostrando la fórmula de cada línea.
5. Señala qué servicio domina el costo y una forma de reducirlo.

## Formato de salida
Guarda el resultado en `docs/costo-piloto.md` con:
- Tabla de supuestos.
- Tabla: servicio, unidad de cobro, precio unitario consultado, cantidad mensual, costo mensual.
- Total mensual y costo por foto analizada.
- Fecha de la consulta y la advertencia: "Estimación con precios públicos de lista; no incluye impuestos, descuentos ni la capa gratuita."
