# Lab 9 · Orquestar, entregar y cerrar

**Módulo 9 · L300 · 25 minutos · Rama de inicio: `lab-09`**

## Qué vas a hacer

Cierras el ciclo de un proyecto real en tres partes:

1. **Delegar una investigación** con un **workflow**: Kiro coordina varios pasos en segundo plano mientras tú sigues trabajando, y entrega un informe de riesgos para llevar el analizador a 50 tiendas.
2. **Llevar los controles al flujo de entrega:** revisas la integración continua que corre pruebas, evaluación, infraestructura y el agente revisor en cada cambio, y ejecutas Kiro CLI en modo **headless** (sin interacción), como lo haría ese pipeline.
3. **Dejar la hoja de ruta** del piloto con tus números y **borrar tu instancia** para no dejar costos.

## Objetivo

Salir del taller con un informe de riesgos, la hoja de ruta del piloto completa y tu cuenta de AWS limpia.

## Antes de empezar

- **Sigues con tu trabajo:** quédate en tu rama.
- **Te atrasaste:**

```bash
git stash --include-untracked
git switch lab-09
pip install -r requirements-dev.txt
```

Asegúrate de estar en la raíz del proyecto (la carpeta `analizador-frescura`).

## Paso a paso

### Paso 1. Lanza un workflow de investigación

En una conversación nueva (**+**), pega:

```text
Usa un workflow para investigar, sin modificar ningún archivo, qué riesgos técnicos, operativos y de costo tiene llevar el analizador de frescura a 50 tiendas. Usa el código, la infraestructura, eval/reporte.md, docs/costo-piloto.md y los documentos de negocio/. Cita archivos, propone una mitigación para cada riesgo y guarda el informe en .kiro/reports/piloto.md.
```

**Resultado esperado:** arriba del chat, el botón **Workflows** muestra un workflow en curso. Haz clic para ver sus pasos. Sigue con el paso 2 mientras corre: tarda unos minutos.

> Si `eval/reporte.md` o `docs/costo-piloto.md` no existen en tu rama, corre `python eval/evaluar.py` o vuelve al paso 6 del Lab 7. El workflow puede trabajar sin ellos, pero el informe será menos concreto.

### Paso 2. Revisa la integración continua

Trae el archivo de GitHub Actions:

```bash
git restore --source final -- .github/workflows/ci.yml
```

> Si clonaste el proyecto de GitHub y no encuentra `final`, usa `origin/final`.

Abre `.github/workflows/ci.yml`. En cada *pull request* corre, en orden:

1. `ruff check .` (estilo)
2. `pytest` (pruebas)
3. `python eval/evaluar.py --minimo 85` (acierto mínimo: si baja de 85%, el cambio no pasa)
4. `cdk synth` (la infraestructura se puede construir)
5. El agente `revisor-seguridad` en modo headless, si el repositorio tiene el secreto `KIRO_API_KEY`

Corre tú los cuatro primeros, igual que el pipeline:

```bash
ruff check .
pytest
python eval/evaluar.py --minimo 85
cd infra
cdk synth -c participante=ci -q
cd ..
```

**Resultado esperado:** los cuatro terminan sin error. Si alguno falla, el pipeline también fallaría: pide a Kiro que lo corrija.

### Paso 3. Ejecuta el revisor en modo headless

En modo headless, Kiro CLI no hace preguntas: recibe el pedido, trabaja con las herramientas que le autorizas y termina con un código de salida. Así se usa dentro de un pipeline.

Si el facilitador te entregó una **KIRO_API_KEY**, configúrala:

macOS o Linux:

```bash
export KIRO_API_KEY=<tu-api-key>
```

Windows (PowerShell):

```powershell
$env:KIRO_API_KEY="<tu-api-key>"
```

Y ejecuta:

```bash
kiro-cli chat --v3 --no-interactive --agent revisor-seguridad --trust-tools=read_file,grep_search "Revisa los cambios del último commit y entrega tu tabla de hallazgos y el veredicto"
```

**Resultado esperado:** la tabla y el veredicto aparecen en la terminal sin que tengas que responder nada. Si no tienes API key, mira la demostración del facilitador.

### Paso 4. Revisa el informe del workflow

Cuando el workflow termine, abre `.kiro/reports/piloto.md`.

**Resultado esperado:** riesgos separados en técnicos, operativos y de costo, cada uno con su archivo de referencia y una mitigación. Por ejemplo: la API no tiene autenticación, las fotos de evaluación son de ejemplo y no de tiendas reales, y el límite de llamadas a Bedrock con 50 tiendas.

### Paso 5. Completa la hoja de ruta del piloto

```bash
git restore --source final -- negocio/hoja-de-ruta-piloto.md
```

En el chat:

```text
Completa la sección "Dónde estamos" de negocio/hoja-de-ruta-piloto.md con los datos de eval/reporte.md, docs/costo-piloto.md y .kiro/reports/piloto.md. No inventes datos: si falta alguno, déjalo en blanco. Deja vacías las columnas de responsable y fecha.
```

Lee el resultado y complétalo con lo que tú decidas: la URL de tu instancia y el próximo paso concreto.

### Paso 6. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 9: informe de riesgos, CI y hoja de ruta del piloto"
```

### Paso 7. Borra tu instancia de AWS

Al final del taller, para no dejar recursos con costo:

```bash
cd infra
cdk destroy -c participante=<tus-iniciales>
```

Cuando pregunte `Are you sure you want to delete: Frescura-<tus-iniciales> (y/n)?`, escribe `y`.

**Resultado esperado:** `Frescura-<tus-iniciales>: destroyed`. Tu web y tu API dejan de responder.

## Criterio de éxito

- [ ] Existe `.kiro/reports/piloto.md` con riesgos y mitigaciones.
- [ ] Los cuatro controles del pipeline pasan en tu computador.
- [ ] `negocio/hoja-de-ruta-piloto.md` tiene tus números y un próximo paso.
- [ ] Tu instancia quedó borrada.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| El botón **Workflows** no muestra nada | Escribe: "Muéstrame el estado del workflow". Si tu cuenta no tiene Workflows, pide el mismo informe sin la palabra "workflow" |
| El workflow modificó archivos | Escribe: "Era una investigación de solo lectura; revierte los cambios" y corre `git status` |
| `cdk destroy` falla por un recurso | Espera un minuto y repítelo. Si sigue fallando, avisa al equipo de AWS |
| El modo headless pide confirmación | Revisa que el comando tenga `--no-interactive` y `--trust-tools` |

## Lo que te llevas

- Un repositorio con specs, steering, hooks, MCP, skills y un agente revisor: la base de cómo trabajará el equipo con agentes.
- Un servicio desplegado y probado con fruta real.
- La medición de acierto, la estimación de costo, el informe de riesgos y la hoja de ruta: el punto de partida del piloto.
