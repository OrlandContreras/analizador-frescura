# Lab 0 · Preparación del equipo

**Antes del taller · unos 30 minutos.** Hazlo con tiempo: si algo no se instala, avisa al equipo organizador antes de la sesión.

## Qué vas a hacer

Instalar las herramientas que usarás en el taller, descargar el proyecto y comprobar que todo funciona. No necesitas saber programar: solo copiar y pegar comandos y comparar lo que ves con el resultado esperado.

## Objetivo

Llegar al taller con Kiro abierto, el proyecto funcionando y acceso a tu cuenta de AWS.

## Qué es cada herramienta

| Herramienta | Para qué la usas |
| --- | --- |
| **Kiro IDE** | El entorno de trabajo con el agente de IA. Aquí pasa casi todo el taller |
| **Kiro CLI** | Kiro en la terminal. Lo usas en los Labs 8 y 9 |
| **Python 3.12 o superior** | El lenguaje del analizador |
| **Node.js 20 o superior** | Lo necesita AWS CDK y los hooks del Lab 6 |
| **Git** | Guarda versiones del proyecto y te permite cambiar de laboratorio |
| **AWS CLI** | Conecta tu computador con tu cuenta de AWS |
| **AWS CDK** | Despliega la solución en AWS con código |
| **uv** | Ejecuta los servidores MCP del Lab 7 |

## Paso a paso

### Paso 1. Instala las herramientas

Instala cada una desde su página oficial. Acepta las opciones por defecto del instalador.

1. **Kiro IDE:** [kiro.dev/downloads](https://kiro.dev/downloads/). Ábrelo e inicia sesión con la cuenta que te indicó el equipo organizador.
2. **Python 3.12 o superior:** [python.org/downloads](https://www.python.org/downloads/). En Windows, marca **Add python.exe to PATH** en la primera pantalla del instalador.
3. **Node.js 20 o superior (versión LTS):** [nodejs.org](https://nodejs.org/).
4. **Git:** [git-scm.com/downloads](https://git-scm.com/downloads).
5. **AWS CLI versión 2:** [docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
6. **uv:** [docs.astral.sh/uv/getting-started/installation](https://docs.astral.sh/uv/getting-started/installation/).

Cierra y vuelve a abrir Kiro después de instalar todo, para que reconozca las herramientas nuevas.

### Paso 2. Abre la terminal de Kiro

En Kiro, menú **Terminal → New Terminal**. Abajo se abre un panel donde escribes comandos. En esta guía, "la terminal" es siempre esta.

> **Si pegas un comando y no pasa nada**, presiona **Enter** una vez más.

### Paso 3. Instala AWS CDK y Kiro CLI

```bash
npm install -g aws-cdk
```

Kiro CLI, en macOS o Linux:

```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

En Windows, sigue las instrucciones de [kiro.dev/downloads](https://kiro.dev/downloads/) para Kiro CLI.

### Paso 4. Comprueba las versiones

Pega estos comandos uno por uno:

```bash
python3 --version
node --version
git --version
aws --version
cdk --version
uv --version
kiro-cli --version
```

En Windows, usa `py --version` en lugar de `python3 --version`.

**Resultado esperado:** cada comando muestra un número de versión. Python debe ser 3.12 o mayor y Node 20 o mayor. Si alguno dice "command not found" o "no se reconoce", reinstálalo y vuelve a abrir Kiro.

### Paso 5. Descarga el proyecto

1. Descarga `analizador-frescura.zip` del enlace que te envió el equipo organizador.
2. Descomprímelo en una carpeta fácil de encontrar, por ejemplo `Documentos/taller-kiro/`.
3. En Kiro, elige **File → Open Folder** y selecciona la carpeta `analizador-frescura`.
4. Si Kiro pregunta si confías en los autores de la carpeta, elige confiar.

**Resultado esperado:** en el explorador de la izquierda ves las carpetas `app`, `infra`, `laboratorios`, `negocio`, `tests` y `web`.

### Paso 6. Prepara el entorno de Python

En la terminal de Kiro (se abre en la carpeta del proyecto):

macOS o Linux:

```bash
git switch lab-01
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Windows (PowerShell):

```powershell
git switch lab-01
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Si Windows dice que no puede ejecutar scripts, corre una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, responde `S` y repite la línea de `Activate.ps1`.

**Resultado esperado:** al inicio de la línea de la terminal aparece `(.venv)`. Eso indica que el entorno está activo.

> **Cada vez que abras una terminal nueva**, actívalo otra vez: `source .venv/bin/activate` (macOS o Linux) o `.venv\Scripts\Activate.ps1` (Windows).

### Paso 7. Corre las pruebas

```bash
pytest
```

**Resultado esperado:** al final dice `32 passed, 1 skipped`. La prueba omitida (*skipped*) es intencional: la activarás en el Lab 4.

### Paso 8. Conecta tu cuenta de AWS

El día del taller, el equipo de AWS te entregará una cuenta y las instrucciones para configurar tus credenciales. Cuando las tengas:

```bash
aws sts get-caller-identity
```

**Resultado esperado:** un JSON con `"Account"` (el número de tu cuenta) y `"Arn"`.

Luego fija la región del taller:

macOS o Linux:

```bash
export AWS_REGION=us-east-1
```

Windows (PowerShell):

```powershell
$env:AWS_REGION="us-east-1"
```

### Paso 9. Inicia sesión en Kiro CLI

```bash
kiro-cli login
```

Sigue las instrucciones que aparecen. Se abre el navegador para que inicies sesión con la misma cuenta de Kiro IDE.

**Resultado esperado:** `kiro-cli whoami` muestra tu cuenta.

## Criterio de éxito

- [ ] Todas las herramientas muestran su versión.
- [ ] `pytest` muestra `32 passed, 1 skipped`.
- [ ] `aws sts get-caller-identity` muestra tu cuenta (el día del taller).
- [ ] `kiro-cli whoami` muestra tu cuenta.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| `pytest` dice "No module named frescura" | Estás fuera de la carpeta del proyecto o sin el entorno activo. Abre la terminal de Kiro con el proyecto abierto y activa `.venv` |
| `pip install` falla por permisos | No uses `sudo`. Revisa que `(.venv)` aparece al inicio de la línea |
| `git switch lab-01` dice que la rama no existe | Descomprimiste otra versión del proyecto. Descarga de nuevo el zip del enlace oficial |
| `aws sts get-caller-identity` da un error de credenciales | Repite la configuración que te indicó el equipo de AWS |
