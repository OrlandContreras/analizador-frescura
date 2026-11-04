# Lab 1 · Primer contacto

**Módulo 1 · L100 · 15 minutos · Rama de inicio: `lab-01`**

## Qué vas a hacer

Vas a conocer el proyecto del taller y a trabajar por primera vez con el agente de Kiro: le pedirás que te explique cómo funciona el analizador, que te muestre dónde se toma cada decisión y que haga un cambio pequeño que luego deshaces.

### El caso

En la sección de frutas y verduras se pierde producto porque se madura en la góndola sin que nadie actúe a tiempo. El **Analizador de frescura** recibe la foto de un banano, aguacate hass, tomate chonto, mango o papaya y responde:

- su **etapa de madurez**: verde, pintón, maduro o sobremaduro;
- los **días** que faltan para su punto óptimo;
- su **información nutricional** por porción.

El producto tiene **dos usuarios**, y en cada laboratorio construyes algo para los dos:

| Vista | Archivo | Quién la usa | Qué ve |
| --- | --- | --- | --- |
| Personal de tienda | `web/index.html` | Auxiliares y jefes de la sección | Todo el análisis y, desde el Lab 3, la acción en tienda |
| Cliente comprador | `web/cliente.html` | Quien compró la fruta | Solo información pública: cuándo estará en su punto y su nutrición |

Un modelo de IA de Amazon Bedrock **describe** la foto (qué producto es y qué tan maduro se ve, de 0 a 100). Las **reglas del negocio**, escritas en el código, **deciden** la etapa. Así cada resultado se puede explicar y auditar.

## Objetivo

Al terminar sabrás abrir el chat de Kiro, pedirle trabajo, ubicar las secciones de su panel y deshacer un cambio del agente con un *checkpoint*.

## Antes de empezar

> **Terminal:** abre la terminal de Kiro (**Terminal → New Terminal**) y activa el entorno de Python. Debe aparecer `(.venv)` al inicio de la línea.
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

1. Terminaste el [Lab 0](../00-preparacion/README.md).
2. Kiro tiene abierta la carpeta `analizador-frescura`.
3. En la terminal de Kiro, con el entorno activo:

```bash
git switch lab-01
```

## Paso a paso

### Paso 1. Comprueba el proyecto

En la terminal:

```bash
pytest
```

**Resultado esperado:** `33 passed, 1 skipped`.

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

### Paso 6. Conoce la vista del cliente

Pega en el chat:

```text
Compara web/index.html y web/cliente.html en una tabla: qué ve el personal, qué ve el cliente y qué archivos comparten las dos páginas.
```

**Resultado esperado:** el personal ve la tienda, la porción, la etapa, los días, la confianza y la nutrición; el cliente ve frases sencillas como "Está pintón" y "Estará en su punto en 2 días", y la nutrición. Las dos páginas comparten `web/estilos.css`, `web/comun.js` y las fotos de muestra de `web/muestras/`.

### Paso 7. Pide un cambio y deshazlo con un checkpoint

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

### Paso 8. Mira el analizador funcionando

El facilitador muestra en pantalla su instancia ya desplegada: toca una de las fotos de muestra en la vista del personal y luego en la del cliente, y compara los resultados. En el Lab 8 harás lo mismo con tu propia instancia.

## Criterio de éxito

- [ ] `pytest` muestra `33 passed, 1 skipped`.
- [ ] Ubicaste las cuatro secciones del panel de Kiro.
- [ ] Kiro respondió con la etapa y los días correctos, citando archivos.
- [ ] Sabes qué ve el personal y qué ve el cliente.
- [ ] Deshiciste un cambio con **Restore** y `git status --short` quedó vacío.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| Kiro responde en inglés | Escribe: "Responde en español de aquí en adelante" |
| No ves **Restore** | Pasa el mouse sobre tu mensaje en el chat; el enlace aparece arriba a la derecha de ese mensaje |
| `git status --short` muestra `app/frescura/reglas.py` | Corre `git restore app/frescura/reglas.py` |
| No ves el ícono de Kiro | Revisa que iniciaste sesión en Kiro IDE |
