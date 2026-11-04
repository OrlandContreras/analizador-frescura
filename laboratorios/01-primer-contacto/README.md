# Lab 1 · Primer contacto

**Módulo 1 · L100 · 15 minutos · Rama de inicio: `lab-01`**

## Qué vas a hacer

Vas a conocer el proyecto del taller y a trabajar por primera vez con el agente de Kiro: le pedirás que te explique cómo funciona el analizador, que te muestre dónde se toma cada decisión y que haga un cambio pequeño que luego deshaces.

### El caso

En la sección de frutas y verduras se pierde producto porque se madura en la góndola sin que nadie actúe a tiempo. El **Analizador de frescura** recibe la foto de un banano, aguacate hass, tomate chonto, mango o papaya y responde:

- su **etapa de madurez**: verde, pintón, maduro o sobremaduro;
- los **días** que faltan para su punto óptimo;
- su **información nutricional** por porción.

Un modelo de IA de Amazon Bedrock **describe** la foto (qué producto es y qué tan maduro se ve, de 0 a 100). Las **reglas del negocio**, escritas en el código, **deciden** la etapa. Así cada resultado se puede explicar y auditar.

## Objetivo

Al terminar sabrás abrir el chat de Kiro, pedirle trabajo, ubicar las secciones de su panel y deshacer un cambio del agente con un *checkpoint*.

## Antes de empezar

1. Terminaste el [Lab 0](../00-preparacion/README.md).
2. Kiro tiene abierta la carpeta `analizador-frescura`.
3. En la terminal de Kiro, con el entorno activo (`(.venv)` al inicio de la línea):

```bash
git switch lab-01
```

## Paso a paso

### Paso 1. Comprueba el proyecto

En la terminal:

```bash
pytest
```

**Resultado esperado:** `32 passed, 1 skipped`.

### Paso 2. Recorre el panel de Kiro

En la barra vertical de la izquierda, haz clic en el ícono del fantasma de Kiro. Ubica estas cuatro secciones; las usarás más adelante:

| Sección | Para qué sirve | Lab |
| --- | --- | --- |
| **SPECS** | Planear una funcionalidad: requisitos, diseño y tareas | 2, 3 y 4 |
| **AGENT HOOKS** | Reglas que se ejecutan solas | 6 |
| **AGENT STEERING & SKILLS** | Contexto de la compañía y procedimientos reutilizables | 5 y 7 |
| **MCP SERVERS** | Conexiones con herramientas externas | 7 |

### Paso 3. Abre el chat

El chat está en el panel de la derecha. Para empezar una conversación nueva, haz clic en el botón **+** de arriba a la derecha de ese panel.

Debajo del cuadro de texto hay un interruptor **Autopilot**:

- **Activado:** Kiro ejecuta comandos y edita archivos sin preguntarte.
- **Desactivado:** te pide aprobar cada acción. Lee qué va a hacer y apruébalo si coincide con lo que pediste.

Las dos formas sirven para el taller.

### Paso 4. Pide que te explique el proyecto

Pega en el chat y presiona **Enter**:

```text
Explica en 5 viñetas qué hace este proyecto, cómo viaja una foto desde el celular hasta la respuesta, y qué decide el modelo de IA y qué deciden las reglas del código.
```

**Resultado esperado:** Kiro lee los archivos y explica que la foto llega por API Gateway a una función Lambda, que el modelo de Bedrock devuelve producto e índice de madurez, que `reglas.py` decide la etapa con los umbrales del catálogo y que el historial se guarda en DynamoDB sin la foto.

### Paso 5. Pide un dato concreto con su fuente

```text
¿Qué etapa de madurez daría el analizador para un banano con índice 65 y cuántos días faltan para su punto? Dime en qué archivo y en qué función se calcula cada cosa.
```

**Resultado esperado:** etapa **maduro** y **0 días**. Kiro señala `app/frescura/reglas.py`, funciones `etapa_madurez` y `dias_hasta_optimo`, y los umbrales del banano en `app/frescura/datos/catalogo.json` (maduro desde 50, sobremaduro desde 80).

### Paso 6. Pide un cambio y deshazlo con un checkpoint

1. Pega:

```text
Agrega un comentario en la primera línea de app/frescura/reglas.py que diga: Prueba del Lab 1.
```

2. Abre `app/frescura/reglas.py` y comprueba que el comentario está.
3. En el chat, sube hasta tu último pedido. Justo encima dice **Checkpoint** y, a la derecha, **Restore**. Haz clic en **Restore** y luego en **Confirm**.
4. En la terminal:

```bash
git status --short
```

**Resultado esperado:** el comentario desapareció del archivo y `git status --short` no muestra ninguna línea: el proyecto quedó como estaba.

### Paso 7. Mira el analizador funcionando

El facilitador muestra en pantalla su instancia ya desplegada: toma con el celular la foto de una fruta de la mesa y aparece el resultado. En el Lab 8 harás lo mismo con tu propia instancia.

## Criterio de éxito

- [ ] `pytest` muestra `32 passed, 1 skipped`.
- [ ] Ubicaste las cuatro secciones del panel de Kiro.
- [ ] Kiro respondió con la etapa y los días correctos, citando archivos.
- [ ] Deshiciste un cambio con **Restore** y `git status --short` quedó vacío.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| Kiro responde en inglés | Escribe: "Responde en español de aquí en adelante" |
| No ves **Restore** | Pasa el mouse sobre tu mensaje en el chat; el enlace aparece arriba a la derecha de ese mensaje |
| `git status --short` muestra `app/frescura/reglas.py` | Corre `git restore app/frescura/reglas.py` |
| No ves el ícono de Kiro | Revisa que iniciaste sesión en Kiro IDE |
