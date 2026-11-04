# Lab 9 · Operar con un Power

**Módulo 9 · L300 · 15 minutos · Rama de inicio: `lab-09`**

## Qué vas a hacer

Un **Power** es un paquete que se instala en Kiro y le da conocimiento experto sobre un tema. Junta en una sola carpeta lo que ya conoces por separado:

| Parte | Qué aporta | Lo viste en |
| --- | --- | --- |
| **Skills** | Instrucciones paso a paso para una tarea, con scripts y material de referencia | Lab 7 |
| **Servidores MCP** (opcional) | Herramientas para conectarse a servicios externos | Lab 7 |
| **Palabras clave** | Cuándo se activa el Power | Nuevo |

La diferencia con lo anterior: un Power **no se carga siempre**. Kiro lee tu pedido y activa solo los Powers relacionados, por sus palabras clave. Así el agente no se llena de herramientas que no necesita. Además, un Power se **instala una vez y sirve en cualquier proyecto**, y se comparte por GitHub.

En este laboratorio usas un Power **que ya viene creado**: `operacion-frescura`, para operar el analizador que desplegaste en el Lab 8. Trae dos skills:

| Skill | Qué hace |
| --- | --- |
| `resumen-uso` | Lee el historial de DynamoDB (solo lectura) y resume el uso por canal (personal y clientes), tienda, producto y etapa |
| `diagnosticar-instancia` | Revisa que la API responda, que la validación de imágenes funcione y si hubo fallos en los registros |

## Objetivo

Entender cómo está hecho un Power, instalarlo desde una carpeta y usarlo para revisar el uso y la salud de tu instancia en AWS, sin escribir ningún comando de AWS.

## Antes de empezar

> **Terminal:** abre la terminal de Kiro (**Terminal → New Terminal**) y activa el entorno de Python. Debe aparecer `(.venv)` al inicio de la línea.
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

- **Sigues con tu trabajo:** trae el Power:

```bash
git restore --source lab-09 powers
```

> Si clonaste el proyecto de GitHub y no encuentra `lab-09`, usa `origin/lab-09`.

- **Te atrasaste:**

```bash
git stash --include-untracked
git switch lab-09
pip install -r requirements-dev.txt
```

Ten a mano tus iniciales, las que usaste en `cdk deploy -c participante=<tus-iniciales>`. Si no lograste desplegar en el Lab 8, igual puedes hacer este laboratorio con datos de ejemplo (te lo indica el paso 4).

## Paso a paso

### Paso 1. Conoce el Power

En el **Explorer**, despliega la carpeta `powers/operacion-frescura`:

```text
powers/operacion-frescura/
├── plugin.json                         ← la ficha del Power
└── skills/
    ├── resumen-uso/
    │   ├── SKILL.md                    ← las instrucciones para el agente
    │   ├── scripts/resumen_uso.py      ← el programa que lee el historial
    │   └── references/historial-ejemplo.json
    └── diagnosticar-instancia/
        ├── SKILL.md
        ├── scripts/diagnosticar.py
        └── references/errores-comunes.md
```

Abre `plugin.json`:

| Campo | Qué significa |
| --- | --- |
| `name` | Identificador del Power, en minúsculas y con guiones |
| `version` | Versión del Power. Al publicar cambios, se sube |
| `description` | Qué hace, en una frase. Kiro la muestra en el panel |
| `author` | Quién lo mantiene |
| `keywords` | **Las palabras que lo activan.** Si tu pedido menciona "historial", "uso por tienda" o "diagnostica", Kiro activa este Power |

Abre `skills/diagnosticar-instancia/SKILL.md`. Tiene la misma estructura que las skills del Lab 7: un encabezado con `name` y `description`, los pasos que debe seguir el agente y sus reglas. Fíjate en la regla: **"No despliegues, no borres ni cambies recursos"**.

> Este Power no trae servidores MCP porque sus skills usan scripts de Python, que funcionan igual en Windows, macOS y Linux. Si un Power los necesita, van en un archivo `mcp.json` junto a `plugin.json`, y Kiro los enciende y apaga junto con el Power.

### Paso 2. Instala el Power

1. En la barra de la izquierda, haz clic en el ícono de **Powers** (el fantasma de Kiro con un rayo).
2. Haz clic en **Add Custom Power**.
3. Elige **Import power from a folder**.
4. Selecciona la carpeta `powers/operacion-frescura` del proyecto y haz clic en **Install**.

**Resultado esperado:** `operacion-frescura` aparece en la lista de Powers instalados. Haz clic sobre él para ver su descripción y sus palabras clave.

> Si Kiro ofrece **Try the power**, puedes usarlo: te guía por un primer uso.

### Paso 3. Pide un diagnóstico de tu instancia

Abre una conversación nueva (**+**) y pega, con tus iniciales en lugar de `<tus-iniciales>`:

```text
Diagnostica la salud de mi instancia del analizador. Mi participante es <tus-iniciales>.
```

**Resultado esperado:**

1. Kiro activa el Power `operacion-frescura` y su skill `diagnosticar-instancia`. Lo ves en la respuesta del chat.
2. Te pide permiso para ejecutar `diagnosticar.py`: acéptalo. El script no envía fotos al modelo ni cambia nada.
3. Entrega una tabla con cuatro comprobaciones (stack, `/salud`, validación de imagen y registros recientes) y un veredicto: **Instancia sana** o **Requiere atención**.

Si algo falla, Kiro explica la causa probable con `references/errores-comunes.md` y el siguiente paso.

### Paso 4. Pide el resumen de uso

En la misma conversación:

```text
¿Cómo va el uso del analizador por tienda? Guarda el resumen en docs/uso-piloto.md.
```

**Resultado esperado:** Kiro usa la skill `resumen-uso`, ejecuta `resumen_uso.py` y crea `docs/uso-piloto.md` con el total de análisis, cuántos vienen del personal y cuántos de clientes, una tabla por tienda y el porcentaje del personal que va a **revisión humana** (confianza menor a 0,70, según la política POL-FRV-001).

> **¿No desplegaste o tu historial está vacío?** Escribe: "Usa los datos de ejemplo del Power". Kiro corre el mismo script con `historial-ejemplo.json`, y el resumen avisa que **no son datos reales**. Con esos datos hay 40 análisis del personal y 12 de clientes, y el 38% de los del personal va a revisión humana, y Kiro debe recomendarlo como el primer punto a mejorar del piloto.

### Paso 5. Comprueba que se activa solo cuando hace falta

Abre una conversación nueva (**+**) y pega:

```text
Explícame en dos líneas qué hace app/frescura/reglas.py.
```

**Resultado esperado:** Kiro responde **sin** activar `operacion-frescura`: tu pedido no tiene nada que ver con operar la instancia. Así funcionan las palabras clave.

### Paso 6 (opcional). Explora el catálogo de Powers

En el panel de **Powers**, en **Available Powers**, busca `aws` con el ícono de la lupa. Haz clic en alguno, por ejemplo uno de AWS SAM o de AWS, y lee su descripción: así se ven los Powers que publican AWS y otras empresas. **No lo instales** durante el taller.

### Paso 7. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 9: Power de operación y resumen de uso"
```

## Criterio de éxito

- [ ] `operacion-frescura` aparece en la lista de Powers instalados.
- [ ] El diagnóstico entregó la tabla de cuatro comprobaciones y un veredicto.
- [ ] Existe `docs/uso-piloto.md` con el uso por tienda.
- [ ] En un pedido que no tiene que ver con la operación, el Power no se activó.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| No ves el ícono de **Powers** | Actualiza Kiro (**Help → Check for Updates**). Si sigue sin aparecer, avisa al facilitador |
| **Import power from a folder** no acepta la carpeta | Elige la carpeta `operacion-frescura` (la que tiene `plugin.json`), no la carpeta `powers` |
| Kiro no activa el Power | Usa las palabras del paso 3: "diagnostica", "salud de mi instancia", "historial", "uso por tienda". También puedes escribir: "Usa el Power operacion-frescura" |
| El script dice `No module named boto3` o `python: command not found` | Kiro usó un Python fuera del entorno del proyecto. Escríbele: "Ejecútalo con .venv\Scripts\python.exe" (Windows) o "Ejecútalo con .venv/bin/python" (macOS o Linux) |
| "No existe el stack Frescura-…" | Revisa tus iniciales: deben ser las mismas del Lab 8. Si no desplegaste, usa los datos de ejemplo (paso 4) |
| `Registros recientes` dice **ATENCIÓN** con `AccessDeniedException` | Bedrock no está habilitado en tu cuenta. Avisa al equipo de AWS |
| El script dice `Unable to locate credentials` | Repite el paso 9 del [Lab 0](../00-preparacion/README.md) |
| Te quedaste sin tiempo | Cambia a la rama `lab-10`, que ya trae el Power y un `docs/uso-piloto.md` con datos de ejemplo |

**Para discutir:** ¿qué tareas repetidas de tu área convendría empaquetar en un Power para que cualquier equipo las use igual?
