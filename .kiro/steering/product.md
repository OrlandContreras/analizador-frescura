---
inclusion: always
---
# Producto: Analizador de frescura de frutas y verduras

## Qué es
Un servicio que, con la foto de una fruta o verdura, indica su etapa de madurez, los días hasta su punto óptimo, la acción recomendada en tienda y su información nutricional por porción.

## Para quién
- **Piloto:** auxiliares y jefes de la sección de frutas y verduras de las tiendas Éxito y Carulla. Objetivo: reducir la pérdida de producto (ver `negocio/necesidad.md`).
- **Fase siguiente:** clientes en la app, que consultan cuándo estará en su punto lo que compraron.

## Reglas del negocio que el agente debe respetar
- Las acciones en tienda siguen la política POL-FRV-001: #[[file:negocio/politica-acciones-tienda.md]]
- El modelo de visión solo **describe**; las **reglas del código deciden** la etapa y la acción. No muevas decisiones de negocio al prompt del modelo.
- Si la confianza es menor a 0,70, la respuesta es **Revisar**: nunca se recomienda una acción con un análisis dudoso.
- Nunca se guarda la foto. El historial solo registra producto, etapa, índice, confianza y tienda.
- Los datos de tienda de este proyecto son ficticios. No agregues datos reales de clientes, precios ni inventario.

## Tono
- Español de Colombia, claro y breve. Mensajes para el personal en imperativo ("Rebajar 30%…").
- Los mensajes para el cliente siguen `.kiro/steering/mensajes-cliente.md`.
