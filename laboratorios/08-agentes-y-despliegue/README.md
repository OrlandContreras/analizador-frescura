# Lab 8 · Agentes especializados y despliegue

**Módulo 8 · L300 · 30 minutos · Rama de inicio: `lab-08`**

## Qué vas a hacer

Antes de desplegar, un revisor de seguridad mira la solución. Vas a crear ese revisor como un **agente especializado**: un agente con un rol, instrucciones propias y permisos limitados. Este solo puede leer y correr comandos de verificación: no puede editar archivos ni desplegar.

Después **despliegas tu propia instancia** del analizador en tu cuenta de AWS y la pruebas con una fruta real desde tu celular. El despliegue lo ejecutas tú: el hook del Lab 6 impide que lo haga el agente.

## Objetivo

Tener tu analizador funcionando en AWS, revisado antes de desplegarse, y analizar una fruta real con el celular.

## Antes de empezar

> **Terminal:** abre la terminal de Kiro (**Terminal → New Terminal**) y activa el entorno de Python. Debe aparecer `(.venv)` al inicio de la línea.
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

- **Sigues con tu trabajo:** quédate en tu rama.
- **Te atrasaste:**

```bash
git stash --include-untracked
git switch lab-08
pip install -r requirements-dev.txt
```

Comprueba en la terminal:

```bash
aws sts get-caller-identity
kiro-cli whoami
```

Los dos deben mostrar tu cuenta. Si no, repite los pasos 8 y 9 del [Lab 0](../00-preparacion/README.md). Fija la región del taller (igual en los dos sistemas):

```bash
aws configure set region us-east-1
```

## Paso a paso

### Paso 1. Trae el agente revisor

```bash
git restore --source lab-09 .kiro/agents/revisor-seguridad.json
```

> Si clonaste el proyecto de GitHub y no encuentra `lab-09`, usa `origin/lab-09`.

Abre `.kiro/agents/revisor-seguridad.json`. Fíjate en:

- `tools`: solo `read` y `shell`. No tiene herramientas para escribir archivos.
- `permissions`: el shell solo puede correr `git`, `pytest`, `ruff check` y `cdk synth`.
- `prompt`: qué revisa y cómo entrega el resultado.

### Paso 2. Pide la revisión de seguridad

Los agentes especializados se usan desde Kiro CLI. En la terminal, desde la raíz del proyecto:

```bash
kiro-cli chat --agent revisor-seguridad
```

Cuando aparezca el cuadro para escribir, pega:

```text
Revisa la infraestructura y el código antes de desplegar.
```

**Resultado esperado:** una tabla de hallazgos con severidad, archivo:línea y sugerencia, y un veredicto final. Como la API del taller no tiene autenticación, es probable que el revisor lo marque: está previsto para el piloto. Para salir de Kiro CLI escribe `/quit`.

### Paso 3. Prepara la cuenta para CDK

```bash
cd infra
cdk bootstrap
```

**Resultado esperado:** termina con `Environment aws://<cuenta>/us-east-1 bootstrapped`. Si el equipo de AWS ya lo hizo, termina en segundos con `(no changes)`.

### Paso 4. Despliega tu instancia

Cambia `<tus-iniciales>` por tus iniciales, en minúscula y sin espacios (por ejemplo `oc`):

```bash
cdk deploy -c participante=<tus-iniciales>
```

1. CDK muestra los permisos que va a crear y pregunta `Do you wish to deploy these changes (y/n)?`. Escribe `y` y presiona **Enter**.
2. Espera unos 5 minutos. Mientras tanto, el facilitador explica qué recursos se están creando.

**Resultado esperado:** al final, en **Outputs**, aparecen:

- `UrlApi`: la dirección de tu API.
- `UrlWeb`: la página para el celular.
- `TablaAnalisis`: la tabla del historial.
- `GrupoRegistros`: dónde quedan los registros de la función.

Copia esos cuatro valores en tu bloc de notas.

### Paso 5. Comprueba que la API responde

Reemplaza `<UrlApi>` por tu valor:

macOS o Linux:

```bash
curl <UrlApi>/salud
```

Windows (PowerShell):

```powershell
curl.exe <UrlApi>/salud
```

**Resultado esperado:** `{"estado": "ok"}`.

### Paso 6. Analiza una fruta real

1. Abre `UrlWeb` en el navegador de tu celular. Puedes enviártela por chat o escribirla.
2. En **Tienda**, escribe `T-<tus-iniciales>`.
3. Toca **Tomar o elegir foto** y fotografía de cerca una fruta de la mesa, con buena luz y una sola fruta en la foto.

**Resultado esperado:** en unos segundos aparece el producto, la etapa, los días hasta su punto, la confianza y la nutrición. Prueba con frutas en distintas etapas. Si la confianza es baja, toma la foto más cerca.

> Si tu rama tiene la acción en tienda del Lab 3, también aparece **Acción en tienda**.

### Paso 7. Comprueba el historial

Reemplaza `<TablaAnalisis>` por tu valor:

```bash
aws dynamodb scan --table-name <TablaAnalisis> --select COUNT
```

**Resultado esperado:** `"Count"` igual al número de fotos que analizaste. El historial guarda producto, etapa, índice, confianza y tienda, nunca la foto.

### Paso 8. Vuelve a la raíz del proyecto

```bash
cd ..
```

## Criterio de éxito

- [ ] El agente revisor entregó su tabla y veredicto sin modificar archivos.
- [ ] `cdk deploy` terminó y mostró los cuatro **Outputs**.
- [ ] Analizaste al menos dos frutas reales desde el celular.
- [ ] La tabla del historial tiene tus análisis.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| `cdk deploy` dice "Falta tu identificador" | Agrega `-c participante=<tus-iniciales>` (de 2 a 10 letras o números, empezando con letra) |
| `cdk deploy` dice `python: command not found` o "python no se reconoce" | El entorno de Python no está activo en esa terminal. Actívalo (ver **Antes de empezar**) y repite el comando dentro de `infra` |
| PowerShell dice "The '<' operator is reserved for future use" | Escribiste los signos `<` y `>`. Usa solo tus iniciales: `cdk deploy -c participante=oc` |
| `cdk deploy` dice que la cuenta no tiene bootstrap | Corre `cdk bootstrap` dentro de `infra` |
| La web dice "No se pudo analizar la imagen" (error 502) | Mira los registros: `aws logs tail <GrupoRegistros> --since 10m`. Si dice `AccessDeniedException`, el modelo de Bedrock no está habilitado en tu cuenta: avisa al equipo de AWS |
| La web dice "Too Many Requests" | Superaste el límite de uso del taller (5 por segundo). Espera unos segundos |
| `kiro-cli chat --agent` no encuentra el agente | Corre el comando desde la raíz del proyecto, donde está `.kiro/agents/` |
| Te quedaste sin tiempo | Pide al facilitador que te muestre su instancia y sigue con el Lab 9; despliega al final si hay tiempo |
