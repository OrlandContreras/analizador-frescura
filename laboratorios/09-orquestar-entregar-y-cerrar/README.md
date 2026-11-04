# Lab 9 · Orquestar, entregar y cerrar

**Módulo 9 · L300 · 25 minutos · Rama de inicio: `lab-09`**

## Qué vas a hacer

Un **workflow** es una receta de trabajo de varios pasos que Kiro ejecuta **en segundo plano** mientras sigues trabajando. Cada paso lo hace un agente distinto, y un paso puede usar el resultado del anterior. Las recetas se guardan como archivos en `.kiro/workflows/` y se pueden reutilizar.

En este laboratorio trabajas con dos workflows:

| Workflow | Quién lo hace | Qué hace |
| --- | --- | --- |
| `investigar-piloto` | **Ya viene creado** | 1 paso: investiga, sin modificar el proyecto, los riesgos de llevar el analizador a más tiendas y escribe un informe |
| `preparar-piloto` | **Lo creas tú** | 2 pasos encadenados: el agente `revisor-seguridad` del Lab 8 revisa la solución y otro agente usa esa revisión para completar la hoja de ruta del piloto |

Mientras los workflows corren, revisas la integración continua del proyecto y, al final, borras tu instancia de AWS.

> Los workflows usan más créditos que una conversación normal. Conviene usarlos para trabajo de varios pasos, no para pedidos cortos.

## Objetivo

Ejecutar un workflow ya creado, crear y ejecutar uno propio que encadena dos agentes, y salir con el informe de riesgos, la hoja de ruta del piloto y tu cuenta de AWS limpia.

## Antes de empezar

> **Terminal:** abre la terminal de Kiro (**Terminal → New Terminal**) y activa el entorno de Python. Debe aparecer `(.venv)` al inicio de la línea.
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

- **Sigues con tu trabajo:** trae el workflow que viene creado, la plantilla de la hoja de ruta y los agentes del Lab 8 (si ya los tienes, no pasa nada):

```bash
git restore --source lab-09 .kiro/workflows/investigar-piloto.workflow.json negocio/hoja-de-ruta-piloto.md .kiro/agents
```

> Si clonaste el proyecto de GitHub y no encuentra `lab-09`, usa `origin/lab-09`.

- **Te atrasaste:**

```bash
git stash --include-untracked
git switch lab-09
pip install -r requirements-dev.txt
```

Si no tienes `eval/reporte.md`, créalo ahora: el informe y la hoja de ruta lo usan.

```bash
python eval/evaluar.py
```

## Paso a paso

### Paso 1. Activa los workflows

1. Abre la paleta de comandos: **Ctrl+Shift+P** (Windows o Linux) o **Cmd+Shift+P** (macOS).
2. Escribe `Workspace Configuration` y elige esa opción.
3. Elige **Workflows** y actívalo.
4. Abre una conversación nueva en el chat (**+**): el cambio aplica a las conversaciones nuevas.

**Resultado esperado:** arriba del chat aparece el botón **Workflows**.

### Paso 2. Conoce el workflow que ya viene creado

Abre `.kiro/workflows/investigar-piloto.workflow.json`:

```json
{
  "name": "investigar-piloto",
  "description": "Investiga, sin modificar el proyecto, los riesgos de llevar el analizador de frescura a más tiendas y escribe un informe con mitigaciones",
  "inputs": {
    "tiendas": "string"
  },
  "steps": [
    {
      "type": "step",
      "id": "investigar",
      "agent": "wf-planner",
      "prompt": "Investigación de solo lectura: ... a {{tiendas}} tiendas. ... Escribe el informe en .kiro/reports/piloto.md ...",
      "artifacts": {
        "informe": ".kiro/reports/piloto.md"
      }
    }
  ]
}
```

| Campo | Qué significa |
| --- | --- |
| `name` | Nombre con el que eliges el workflow al ejecutarlo |
| `inputs` | Datos que Kiro te pide al ejecutarlo. Aquí, `tiendas` |
| `steps` | Los pasos, en orden |
| `type: "step"` | Un paso que ejecuta un agente en su propia sesión |
| `id` | Nombre único del paso |
| `agent` | Qué agente hace el paso. `wf-planner` es un agente de Kiro para investigar y planear |
| `prompt` | La instrucción del paso. `{{tiendas}}` se reemplaza por lo que escribas al ejecutarlo |
| `artifacts` | Archivos que produce el paso |

### Paso 3. Ejecuta el workflow ya creado

1. En la conversación nueva, escribe `/workflow-run` y presiona **Enter**.
2. Elige **investigar-piloto**.
3. Cuando pida `tiendas`, escribe `50`.
4. Si Kiro muestra el plan para aprobarlo, apruébalo.

**Resultado esperado:** el botón **Workflows** muestra un workflow en curso. Haz clic, despliega la ejecución y selecciona el paso **investigar** para ver lo que está haciendo. Tarda unos minutos: **sigue con el paso 4 mientras corre.**

### Paso 4. Mientras tanto: revisa la integración continua

Trae el archivo de GitHub Actions:

```bash
git restore --source final .github/workflows/ci.yml
```

> Si clonaste el proyecto de GitHub y no encuentra `final`, usa `origin/final`.

Abre `.github/workflows/ci.yml`. En cada *pull request* corre, en orden: `ruff check .`, `pytest`, `python eval/evaluar.py --minimo 85` (si el acierto baja de 85%, el cambio no pasa), `cdk synth` y el agente `revisor-seguridad` en modo headless.

Corre tú los cuatro primeros, igual que el pipeline:

```bash
ruff check .
pytest
python eval/evaluar.py --minimo 85
cd infra
cdk synth -c participante=ci -q
cd ..
```

**Resultado esperado:** los cuatro terminan sin error.

### Paso 5. Revisa el informe de riesgos

Cuando el workflow `investigar-piloto` termine, abre `.kiro/reports/piloto.md`.

**Resultado esperado:** riesgos separados en técnicos, operativos y de costo, cada uno con su archivo de referencia y una mitigación. Por ejemplo: la API no tiene autenticación, las fotos de evaluación son de ejemplo y no de tiendas reales, y el límite de llamadas a Bedrock con 50 tiendas.

### Paso 6. Crea tu propio workflow: "preparar-piloto"

Tu workflow tiene **dos pasos encadenados**:

1. `revisar`: el agente **`revisor-seguridad`**, el que usaste en el Lab 8, revisa la solución. No modifica nada.
2. `hoja-de-ruta`: el agente **`wf-coder`** recibe la revisión del paso 1 con `{{previous.output}}` y completa `negocio/hoja-de-ruta-piloto.md`.

**6.1. Crea el archivo vacío.**

1. En la barra de la izquierda, abre el **Explorer**.
2. Despliega la carpeta `.kiro` y luego `workflows`.
3. Haz clic derecho sobre la carpeta `workflows` y elige **New File…**
4. Escribe el nombre `preparar-piloto.workflow.json` y presiona **Enter**.

**Resultado esperado:** se abre un archivo vacío dentro de `.kiro/workflows/`, junto a `investigar-piloto.workflow.json`.

**6.2. Escribe el workflow.** Copia y pega este contenido:

```json
{
  "name": "preparar-piloto",
  "description": "Revisa la seguridad del analizador y completa la hoja de ruta del piloto con esa revisión y el informe de riesgos",
  "inputs": {
    "url_instancia": "string"
  },
  "steps": [
    {
      "type": "step",
      "id": "revisar",
      "agent": "revisor-seguridad",
      "prompt": "Revisa la infraestructura y el código del analizador de frescura antes del piloto. No modifiques archivos. Entrega tu tabla de hallazgos con severidad y tu veredicto."
    },
    {
      "type": "step",
      "id": "hoja-de-ruta",
      "agent": "wf-coder",
      "prompt": "Completa la sección \"Dónde estamos\" de negocio/hoja-de-ruta-piloto.md. Usa la URL de la instancia {{url_instancia}}, el acierto de eval/reporte.md y el costo de docs/costo-piloto.md si existen, los riesgos de .kiro/reports/piloto.md y este resultado de la revisión de seguridad: {{previous.output}} No inventes datos: si falta alguno, déjalo en blanco. Deja vacías las columnas de responsable y fecha. No modifiques ningún otro archivo.",
      "artifacts": {
        "hoja_de_ruta": "negocio/hoja-de-ruta-piloto.md"
      }
    }
  ]
}
```

**6.3. Lee lo que acabas de escribir.** Compáralo con el workflow del paso 2:

| Parte | Valor en tu workflow | Por qué |
| --- | --- | --- |
| `inputs` | `url_instancia` | Kiro te la pide al ejecutarlo y la pone donde dice `{{url_instancia}}` |
| Paso `revisar` → `agent` | `revisor-seguridad` | Tu propio agente del Lab 8: solo lee, no edita ni despliega |
| Paso `hoja-de-ruta` → `agent` | `wf-coder` | Un agente de Kiro que sí puede escribir archivos |
| `{{previous.output}}` | En el segundo paso | Se reemplaza por la respuesta final del paso anterior: así el segundo agente recibe la revisión |
| `artifacts` | `negocio/hoja-de-ruta-piloto.md` | El archivo que produce el segundo paso |

**6.4. Guarda el archivo** con **Ctrl+S** (Windows o Linux) o **Cmd+S** (macOS).

**6.5. Comprueba que el JSON es válido.** En la terminal:

```bash
python -m json.tool .kiro/workflows/preparar-piloto.workflow.json
```

**Resultado esperado:** se imprime el contenido ordenado, sin errores. Si aparece `Expecting ',' delimiter` o un error parecido, compara la línea que indica con el contenido del paso 6.2.

**6.6. Pide a Kiro que valide la receta.** En el chat:

```text
Valida el workflow .kiro/workflows/preparar-piloto.workflow.json con validate_workflow y dime si tiene errores. No lo ejecutes todavía.
```

**Resultado esperado:** Kiro informa que la receta es válida. Si informa un error, corrígelo según lo que indique.

**6.7. Ejecútalo.**

1. En el chat, escribe `/workflow-run` y presiona **Enter**.
2. Elige **preparar-piloto**.
3. Cuando pida `url_instancia`, escribe el valor de `UrlWeb` que copiaste en el Lab 8. Si no desplegaste, escribe `sin desplegar`.
4. Si Kiro muestra el plan para aprobarlo, apruébalo.

**Resultado esperado:** en **Workflows** ves la ejecución con sus dos pasos. Primero corre **revisar** y, cuando termina, **hoja-de-ruta**. Selecciona cada paso para ver qué hizo: en **hoja-de-ruta** verás que el agente recibió la revisión de seguridad.

**6.8. Revisa el resultado.** Abre `negocio/hoja-de-ruta-piloto.md`.

**Resultado esperado:** la sección **Dónde estamos** tiene la URL de tu instancia, el acierto, el costo (si lo calculaste en el Lab 7) y el veredicto de la revisión de seguridad. Lo que faltaba quedó en blanco. Completa tú el **próximo paso concreto**.

### Paso 7 (opcional). Ejecuta el revisor en modo headless

En modo headless, Kiro CLI no hace preguntas: recibe el pedido, trabaja con las herramientas que le autorizas y termina con un código de salida. Así se usa dentro del pipeline.

Si el facilitador te entregó una **KIRO_API_KEY**, configúrala:

Windows (PowerShell):

```powershell
$env:KIRO_API_KEY="<tu-api-key>"
```

macOS o Linux:

```bash
export KIRO_API_KEY=<tu-api-key>
```

Y ejecuta (igual en los dos sistemas):

```bash
kiro-cli chat --v3 --no-interactive --agent revisor-seguridad --trust-tools=read_file,grep_search "Revisa los cambios del último commit y entrega tu tabla de hallazgos y el veredicto"
```

**Resultado esperado:** la tabla y el veredicto aparecen sin que respondas nada. Si no tienes API key, mira la demostración del facilitador.

### Paso 8. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 9: workflows, CI y hoja de ruta del piloto"
```

### Paso 9. Borra tu instancia de AWS

Al final del taller, para no dejar recursos con costo. Reemplaza `<tus-iniciales>` sin los signos `<` y `>`:

```bash
cd infra
cdk destroy -c participante=<tus-iniciales>
```

Cuando pregunte `Are you sure you want to delete: Frescura-<tus-iniciales> (y/n)?`, escribe `y`.

**Resultado esperado:** `Frescura-<tus-iniciales>: destroyed`. Tu web y tu API dejan de responder.

## Criterio de éxito

- [ ] Ejecutaste `investigar-piloto` y existe `.kiro/reports/piloto.md`.
- [ ] **Creaste** `.kiro/workflows/preparar-piloto.workflow.json`, es válido y se ejecutó con sus dos pasos.
- [ ] `negocio/hoja-de-ruta-piloto.md` tiene tus datos y el veredicto de la revisión.
- [ ] Los cuatro controles del pipeline pasan en tu computador.
- [ ] Tu instancia quedó borrada.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| No aparece **Workspace Configuration** ni la opción **Workflows** | Tu versión de Kiro o tu cuenta no tiene workflows. Avisa al facilitador y sigue con el paso 4 |
| `/workflow-run` no muestra tus workflows | Revisa que los archivos estén en `.kiro/workflows/` y terminen en `.workflow.json`. Abre una conversación nueva |
| El workflow falla con "agent not found" en el paso `revisar` | Falta el agente del Lab 8. Corre el `git restore` de **Antes de empezar** |
| El JSON da error en el paso 6.5 | Revisa la línea indicada: suele faltar una coma entre campos o una comilla de cierre |
| El workflow modificó otros archivos | Corre `git status` y revierte lo que no corresponda con `git restore <archivo>` |
| La hoja de ruta tiene datos inventados | Escribe en el chat: "Quita de la hoja de ruta todo dato que no venga de eval/reporte.md, docs/costo-piloto.md, .kiro/reports/piloto.md o la revisión de seguridad" |
| `cdk destroy` falla por un recurso | Espera un minuto y repítelo. Si sigue fallando, avisa al equipo de AWS |
| El modo headless pide confirmación | Revisa que el comando tenga `--no-interactive` y `--trust-tools` |

## Lo que te llevas

- Un repositorio con specs, steering, hooks, MCP, skills, dos agentes y dos workflows: la base de cómo trabajará el equipo con agentes.
- Un servicio desplegado y probado con fruta real.
- La medición de acierto, la estimación de costo, el informe de riesgos y la hoja de ruta: el punto de partida del piloto.

**Para discutir:** ¿qué tareas del área justifican un workflow en vez de un pedido en el chat?
