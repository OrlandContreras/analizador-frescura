# Hoja de ruta: del workshop al piloto y a producción

> **Plantilla del Lab 10.** Complétala con los resultados de tu taller: el acierto de `eval/reporte.md`, el costo de `docs/costo-piloto.md`, el uso de `docs/uso-piloto.md` y los riesgos de `.kiro/reports/piloto.md`.

## Dónde estamos (fin del workshop)

| Elemento | Estado | Evidencia |
| --- | --- | --- |
| Servicio desplegado en AWS | Sí / No | URL de mi instancia: |
| Acción en tienda según POL-FRV-001 | Sí / No | `tests/test_acciones.py` |
| Acierto de etapa (fotos de ejemplo) | ___ % | `eval/reporte.md` |
| Costo mensual estimado para 5 tiendas | USD ___ | `docs/costo-piloto.md` |
| Uso de la instancia | ___ análisis; ___ % a revisión humana | `docs/uso-piloto.md` (Power `operacion-frescura`) |
| Revisión de seguridad antes de desplegar | Veredicto: | Agente `revisor-seguridad` |

## Etapa 1 — Piloto (3 a 5 tiendas, 3 meses)

| Qué | Por qué | Responsable |
| --- | --- | --- |
| Tomar 300 fotos reales por producto en las tiendas piloto y etiquetarlas con el área de frutas y verduras | Medir el acierto con la luz y las variedades reales | |
| Validar umbrales y nutrición con el área y con la tabla del ICBF | Hoy son valores de referencia | |
| Pantalla para que el jefe de sección confirme los casos "Revisar" y "Donar" | La política exige confirmación humana | |
| Tablero de uso: análisis por tienda, acciones y casos "Revisar" | Medir los indicadores del piloto | |
| Autenticación del personal | La API del taller es abierta | |

**Indicadores para pasar a producción:** acierto de etapa ≥ 85% con fotos reales, pérdida de la sección del 8% al 6,5%, menos del 15% de casos "Revisar".

## Etapa 2 — Producción

- Integración con inventario y con el sistema de rebajas para aplicar el descuento automáticamente.
- Más productos del catálogo de frutas y verduras.
- Evaluación continua del modelo con fotos nuevas cada mes.
- Ambientes separados (desarrollo, pruebas, producción) con el pipeline de integración continua del Lab 9.

## Etapa 3 — Clientes en la app

- "¿Cuándo estará listo mi aguacate?" e información nutricional por porción en la app de Éxito y Carulla.
- Revisión legal de los mensajes nutricionales según la normativa colombiana de etiquetado.

## Próximo paso concreto

| Acción | Responsable | Fecha |
| --- | --- | --- |
| | | |
