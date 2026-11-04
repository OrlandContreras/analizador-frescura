---
name: ficha-producto
description: Genera la ficha de un producto del analizador de frescura (umbrales de madurez, días hasta el punto, acción en tienda por etapa, nutrición por porción y lo que ve el cliente). Úsalo cuando pidan la ficha, el resumen o la hoja de un producto como banano, aguacate hass, tomate chonto, mango o papaya.
---
# Ficha de producto

Arma la ficha **solo con datos del proyecto**. No inventes valores.

## Fuentes
1. Umbrales, velocidad de maduración y destino de transformación: `app/frescura/datos/catalogo.json`
2. Nutrición por 100 g y su fuente: `app/frescura/datos/nutricion.json`
3. Acciones en tienda: `negocio/politica-acciones-tienda.md`
4. Tono para el cliente: `.kiro/steering/mensajes-cliente.md`

## Formato

```markdown
# Ficha: <Nombre del producto>

## Madurez
| Etapa | Índice | Acción en tienda |
| --- | --- | --- |
| Verde | 0 a <pinton - 1> | Mantener |
| Pintón | <pinton> a <maduro - 1> | Mantener |
| Maduro | <maduro> a <sobremaduro - 1> | Priorizar |
| Sobremaduro | <sobremaduro> a 100 | Rebajar, transformar o donar según manchas |

Velocidad de maduración: <n> puntos por día. Desde verde (índice 0) llega a su punto en <días> días.
Si se transforma: <destino del catálogo>.

## Nutrición por porción de 100 g
| Energía | Fibra | Potasio | Vitamina C |
| --- | --- | --- | --- |
Fuente: <fuente>. Valores aproximados de referencia.

## Para la vista del cliente (`web/cliente.html`)
| Etapa | Lo que ve el cliente |
| --- | --- |
| Verde | Todavía está verde. Estará en su punto en <días> días. |
| Pintón | Está pintón. Estará en su punto en <días> días. |
| Maduro | Está en su punto. Disfrútalo hoy o mañana. |
| Sobremaduro | Ya pasó su mejor punto. Aprovéchalo hoy en jugos, batidos o preparaciones. |

Mensaje de ejemplo: <una o dos frases, siguiendo mensajes-cliente.md>. Recuerda: el cliente nunca ve la acción en tienda.
```

Calcula los días como `ceil(maduro / velocidad)` y muestra el cálculo.
