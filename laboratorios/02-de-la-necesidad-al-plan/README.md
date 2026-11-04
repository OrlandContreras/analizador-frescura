# Lab 2 · De la necesidad al plan

**Módulo 2 · L100 · 25 minutos · Rama de inicio: `lab-02`**

## Qué vas a hacer

El analizador ya dice en qué etapa está un producto, pero el personal de la tienda necesita saber **qué hacer** con él. La compañía tiene una política para eso: `negocio/politica-acciones-tienda.md` (POL-FRV-001).

En este laboratorio no escribes código. La misma política dice, en su sección 6, **qué puede ver el cliente** comprador. Con Kiro conviertes esa política en una **spec** que cubre a los dos usuarios: un plan de tres documentos que el agente sigue después para construir.

| Documento | Qué contiene |
| --- | --- |
| `requirements.md` | Qué debe hacer el sistema, en requisitos que se comprueban con un sí o un no |
| `design.md` | Cómo se va a construir |
| `tasks.md` | La lista de tareas para construirlo |

**Concepto clave: el formato EARS.** Cada requisito se escribe como `WHEN <situación> THE <sistema> SHALL <comportamiento>`. Por ejemplo: "WHEN la confianza es menor a 0,70, THE Analizador SHALL recomendar Revisar". Así nadie lo interpreta distinto.

## Objetivo

Tener una spec completa de la **acción recomendada en tienda** y de la **vista del cliente**, con requisitos verificables, diseño y como máximo 8 tareas, lista para construirse en el Lab 3.

## Antes de empezar

> **Terminal:** abre la terminal de Kiro (**Terminal → New Terminal**) y activa el entorno de Python. Debe aparecer `(.venv)` al inicio de la línea.
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

En la terminal de Kiro, con el entorno activo:

```bash
git switch lab-02
```

Si vienes del Lab 1 sin cambios pendientes, basta con ese comando. Si tienes cambios, sigue las instrucciones de [Cómo funcionan las ramas](../README.md#cómo-funcionan-las-ramas).

## Paso a paso

### Paso 1. Lee la política

Abre `negocio/politica-acciones-tienda.md` y lee dos secciones:

- **3. Reglas, en este orden:** 7 reglas para el personal; la primera que se cumple decide la acción.
- **6. Lo que ve el cliente:** el cliente solo ve información del producto, nunca la acción en tienda ni la confianza, y si la foto no es clara se le pide otra.

### Paso 2. Crea la spec

1. Abre el panel de Kiro (ícono del fantasma). En la sección **SPECS**, haz clic en **Create New Spec**.
2. Arriba se abre un cuadro que dice *Enter your idea to generate requirement, design, and task specs*. Pega esta descripción y presiona **Enter**:

```text
Agregar al análisis la acción recomendada en tienda para el personal de frutas y verduras, según la política negocio/politica-acciones-tienda.md (mantener, priorizar, rebajar, transformar, donar, retirar o revisar), con revisión humana cuando la confianza sea menor a 0,70, y la vista del cliente de la sección 6 de la política, que nunca muestra información interna. Sin cambiar la infraestructura.
```

3. En el chat aparece **Input required** con tres opciones. Elige **Build a Feature** y haz clic en **Submit answer**.
4. Aparece otra pregunta: *¿Con qué quieres empezar?* Elige **Requirements** y haz clic en **Submit answer**.
5. Espera de 2 a 3 minutos mientras Kiro lee el proyecto y escribe los requisitos.

**Resultado esperado:** en la sección **SPECS** aparece tu spec, con un nombre que elige Kiro (por ejemplo `accion-en-tienda`). Al final de su respuesta, Kiro ofrece en el chat tres opciones: **Generar diseño técnico**, **Generar lista de tareas** y **Analizar requerimientos**. Pueden aparecer en inglés.

### Paso 3. Revisa los requisitos

1. En la sección **SPECS**, haz clic en tu spec y luego en **Requirements**.
2. Comprueba que estas cuatro reglas estén escritas en formato EARS:
   - Confianza menor a 0,70 → Revisar.
   - Moho → Retirar.
   - Maduro → Priorizar.
   - Sobremaduro con 60% o más de manchas → Donar.
   - Vista del cliente → nunca incluye la acción en tienda ni la confianza (un requisito con `SHALL NOT`).

### Paso 4. Pide a Kiro que los analice

1. En el chat, haz clic en la opción **Analizar requerimientos**. Tarda de 2 a 3 minutos.
2. Kiro puede señalar ambigüedades o responder que no encontró ninguna. En los dos casos, escribe esta decisión:

```text
Decisión de negocio: los límites son inclusivos. Confianza de exactamente 0,70 no va a revisión; manchas de exactamente 30% ya es transformar y de exactamente 60% ya es donar. Actualiza los requisitos con esta decisión.
```

**Resultado esperado:** Kiro actualiza `requirements.md` y los límites quedan explícitos (0,70; 30%; 60%).

### Paso 5. Genera el diseño

Haz clic en la opción **Generar diseño técnico** del chat. Tarda de 3 a 4 minutos. Luego abre **Design** desde tu spec y comprueba que diga:

- [ ] En qué archivo nuevo van las reglas (por ejemplo `app/frescura/acciones.py`).
- [ ] Que la respuesta del análisis tendrá un campo `accion`.
- [ ] Cómo se va a probar cada regla, incluidos los límites.
- [ ] Cómo se filtra la respuesta para la vista del cliente (por ejemplo, `app/frescura/vista_cliente.py`).

Si falta algo, pídelo en el chat antes de seguir.

### Paso 6. Genera las tareas, acotadas

En lugar de hacer clic en **Generar lista de tareas**, escribe en el chat:

```text
Genera la lista de tareas con máximo 8 tareas. Las pruebas son obligatorias, no opcionales: no marques ninguna tarea con asterisco.
```

**Resultado esperado:** `tasks.md` con 8 tareas o menos, ninguna marcada con `*`. Ábrelo desde **Tasks** en tu spec.

> **Por qué acotamos:** las tareas marcadas con `*` son opcionales y casi siempre son las pruebas. Sin pruebas, en el Lab 3 no sabrías si lo construido funciona. Y menos tareas significa que se construye en menos tiempo y con menos créditos.

### Paso 7. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 2: spec de la acción en tienda y la vista del cliente"
```

## Criterio de éxito

- [ ] Existen `requirements.md`, `design.md` y `tasks.md` en `.kiro/specs/<nombre-de-tu-spec>/`.
- [ ] Las 7 reglas de la política están como requisitos EARS, con los límites explícitos.
- [ ] Hay un requisito para la vista del cliente.
- [ ] `tasks.md` tiene 8 tareas o menos y las pruebas son obligatorias.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| No ves la opción **Analizar requerimientos** | Escribe en el chat: "Analiza los requisitos y señala ambigüedades, contradicciones y vacíos" |
| Kiro empieza a escribir código | Escribe: "Todavía no implementes nada; solo genera la spec" |
| La spec no menciona la política | Escribe: "Usa como fuente negocio/politica-acciones-tienda.md y actualiza los requisitos" |
| Te quedaste sin tiempo | Cambia a la rama `lab-03`: trae una spec de referencia en `.kiro/specs/accion-en-tienda/` |

**Para discutir:** ¿qué decidiste tú y qué decidió el agente?
