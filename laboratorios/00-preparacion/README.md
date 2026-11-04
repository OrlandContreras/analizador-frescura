# Lab 0 · Preparación del equipo

**Antes del taller · unos 30 a 45 minutos.** Hazlo con tiempo: si algo no se instala, avisa al equipo organizador antes de la sesión. En equipos de la empresa, algunos instaladores pueden necesitar permisos de administrador: pídelos con anticipación a tu área de TI.

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
| **pnpm** | Instala las herramientas de JavaScript (AWS CDK) con controles de seguridad: no ejecuta scripts de instalación que nadie aprobó y evita versiones publicadas hace menos de 24 horas |
| **Git** | Guarda versiones del proyecto y te permite cambiar de laboratorio |
| **AWS CLI** | Conecta tu computador con tu cuenta de AWS |
| **AWS CDK** | Despliega la solución en AWS con código |
| **uv** | Ejecuta los servidores MCP del Lab 7 |

## Sistema operativo

Cada comando de estas guías aparece para tu sistema:

- **Windows:** la terminal de Kiro abre **PowerShell**. Todos los comandos marcados "Windows (PowerShell)" son para ella. Se requiere **Windows 11** para Kiro CLI.
- **macOS o Linux:** la terminal de Kiro abre `zsh` o `bash`. Usa los comandos marcados "macOS o Linux".

Cuando un comando es igual en los dos sistemas, aparece una sola vez.

> **Importante en PowerShell:** donde la guía diga `<tus-iniciales>` o `<UrlApi>`, reemplaza **también los signos `<` y `>`**. Por ejemplo, `participante=<tus-iniciales>` se escribe `participante=oc`. Si dejas los signos, PowerShell muestra el error "The '<' operator is reserved for future use".

## Paso a paso

### Paso 1. Instala las herramientas con instalador

Instala cada una desde su página oficial y acepta las opciones por defecto.

| Herramienta | Dónde descargarla | Nota para Windows |
| --- | --- | --- |
| Kiro IDE | [kiro.dev/downloads](https://kiro.dev/downloads/) | Ábrelo e inicia sesión con la cuenta que te indicó el equipo organizador |
| Python 3.12 o superior | [python.org/downloads](https://www.python.org/downloads/) | En la primera pantalla del instalador, marca **Add python.exe to PATH** |
| Node.js 20 o superior (LTS) | [nodejs.org](https://nodejs.org/) | Acepta las opciones por defecto |
| Git | [git-scm.com/downloads](https://git-scm.com/downloads) | Acepta las opciones por defecto |
| AWS CLI versión 2 | [Instalar AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) | Usa el instalador MSI de 64 bits |

**Cierra Kiro por completo y vuelve a abrirlo** después de instalar todo, para que reconozca las herramientas nuevas.

### Paso 2. Abre la terminal de Kiro

En Kiro, menú **Terminal → New Terminal**. Abajo se abre un panel donde escribes comandos. En esta guía, "la terminal" es siempre esta.

> **Si pegas un comando y no pasa nada**, presiona **Enter** una vez más.

### Paso 3. Instala pnpm, AWS CDK, uv y Kiro CLI

**3.1. pnpm.** En este taller, las herramientas de JavaScript se instalan con pnpm, no con npm.

Windows (PowerShell). La documentación de pnpm recomienda instalarlo con npm en Windows, porque Windows Defender puede bloquear el instalador directo. Es el único uso de npm en el taller:

```powershell
npm install -g pnpm@latest
```

macOS o Linux:

```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

**3.2. Prepara la carpeta de herramientas globales de pnpm** (igual en los dos sistemas):

```bash
pnpm setup
```

Luego **cierra Kiro por completo, vuelve a abrirlo** y abre otra vez la terminal (**Terminal → New Terminal**).

**3.3. AWS CDK con pnpm** (igual en los dos sistemas):

```bash
pnpm add -g aws-cdk
```

**Resultado esperado:** termina con `+ aws-cdk 2.x.x` y `Done`. Si aparece un error, búscalo en **Problemas con pnpm**, al final de esta guía.

**3.4. uv.**

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS o Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**3.5. Kiro CLI.**

Windows 11 (PowerShell):

```powershell
irm 'https://cli.kiro.dev/install.ps1' | iex
```

macOS o Linux:

```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

Al terminar, **cierra Kiro por completo y vuelve a abrirlo** una vez más.

### Paso 4. Comprueba las versiones

Pega estos comandos uno por uno. El primero depende del sistema:

Windows (PowerShell):

```powershell
py --version
```

macOS o Linux:

```bash
python3 --version
```

Los demás son iguales en los dos sistemas:

```bash
node --version
pnpm --version
git --version
aws --version
cdk --version
uv --version
kiro-cli --version
```

**Resultado esperado:** cada comando muestra un número de versión. Python debe ser 3.12 o mayor y Node 20 o mayor. Si alguno dice "command not found" o "no se reconoce como nombre de un cmdlet", reinstálalo y vuelve a abrir Kiro.

### Paso 5. Identifícate en Git

Git necesita tu nombre y correo para guardar versiones. Hazlo una sola vez (igual en los dos sistemas):

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.correo@empresa.com"
```

### Paso 6. Descarga el proyecto

1. Descarga `analizador-frescura.zip` del enlace que te envió el equipo organizador.
2. Descomprímelo en una carpeta de ruta corta:
   - **Windows:** `C:\taller-kiro\`. Evita carpetas sincronizadas con OneDrive y rutas largas.
   - **macOS o Linux:** `~/taller-kiro/`.
3. En Kiro, elige **File → Open Folder** y selecciona la carpeta `analizador-frescura`.
4. Si Kiro pregunta si confías en los autores de la carpeta, elige confiar.

**Resultado esperado:** en el explorador de la izquierda ves las carpetas `app`, `infra`, `laboratorios`, `negocio`, `tests` y `web`.

### Paso 7. Prepara el entorno de Python

En la terminal de Kiro (se abre en la carpeta del proyecto):

Windows (PowerShell):

```powershell
git switch lab-01
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Si PowerShell dice que no puede ejecutar scripts ("running scripts is disabled on this system"), corre una vez el comando siguiente, responde `S` (o `Y`) y repite la línea de `Activate.ps1`:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

macOS o Linux:

```bash
git switch lab-01
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

**Resultado esperado:** al inicio de la línea de la terminal aparece `(.venv)`. Eso indica que el entorno está activo. A partir de aquí, el comando `python` funciona igual en los dos sistemas.

> **Cada vez que abras una terminal nueva, activa el entorno otra vez:**
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

### Paso 8. Corre las pruebas

```bash
pytest
```

**Resultado esperado:** al final dice `32 passed, 1 skipped`. La prueba omitida (*skipped*) es intencional: la activarás en el Lab 4.

### Paso 9. Conecta tu cuenta de AWS

El día del taller, el equipo de AWS te entregará una cuenta y las instrucciones para configurar tus credenciales. Cuando las tengas, fija la región del taller y comprueba la conexión (igual en los dos sistemas):

```bash
aws configure set region us-east-1
aws sts get-caller-identity
```

**Resultado esperado:** un JSON con `"Account"` (el número de tu cuenta) y `"Arn"`.

### Paso 10. Inicia sesión en Kiro CLI

```bash
kiro-cli login
```

Se abre el navegador para que inicies sesión con la misma cuenta de Kiro IDE. Si el navegador no vuelve a la terminal, usa `kiro-cli login --use-device-flow`: muestra una dirección y un código para ingresar.

Comprueba la instalación:

```bash
kiro-cli doctor
```

**Resultado esperado:** `Everything looks good!`

## Criterio de éxito

- [ ] Todas las herramientas muestran su versión.
- [ ] Git tiene tu nombre y correo.
- [ ] `pytest` muestra `32 passed, 1 skipped`.
- [ ] `aws sts get-caller-identity` muestra tu cuenta (el día del taller).
- [ ] `kiro-cli doctor` dice `Everything looks good!`

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| `pytest` dice "No module named frescura" | Estás fuera de la carpeta del proyecto o sin el entorno activo. Abre la terminal de Kiro con el proyecto abierto y activa `.venv` |
| `pip install` falla por permisos | No uses `sudo` ni PowerShell como administrador. Revisa que `(.venv)` aparece al inicio de la línea |
| `git switch lab-01` dice que la rama no existe | Descomprimiste otra versión del proyecto. Descarga de nuevo el zip del enlace oficial |
| `git commit` dice "Please tell me who you are" | Haz el paso 5 |
| `aws sts get-caller-identity` da un error de credenciales | Repite la configuración que te indicó el equipo de AWS |
| Windows: al escribir `python` o `py` se abre la Microsoft Store | Python no quedó instalado o no está en el PATH. Reinstálalo marcando **Add python.exe to PATH**. Si sigue, en **Configuración → Aplicaciones → Configuración avanzada de aplicaciones → Alias de ejecución de aplicaciones**, apaga los alias de `python.exe` y `python3.exe` |
| Windows: `pip install` falla con un error de ruta demasiado larga | Mueve la carpeta del proyecto a `C:\taller-kiro\` y repite el paso 7 |
| Windows: el instalador de Kiro CLI cierra la terminal sin mensaje | Suele ser falta de permisos de administrador. Pide a TI que lo instale o que te dé permisos, y repite el paso 3.5 |
| `kiro-cli` no se reconoce después de instalarlo | Cierra Kiro por completo y vuelve a abrirlo. Si sigue igual, corre `kiro-cli doctor` desde una terminal nueva |

### Problemas con pnpm

| Síntoma | Qué hacer |
| --- | --- |
| `pnpm` no se reconoce | Cierra Kiro por completo y vuelve a abrirlo. Si sigue igual, repite el paso 3.1 |
| `ERR_PNPM_GLOBAL_BIN_DIR_NOT_IN_PATH` ("The configured global bin directory … is not in PATH") | No corriste `pnpm setup`, o la terminal no cargó su configuración. Corre `pnpm setup`, cierra Kiro por completo, vuelve a abrirlo y repite `pnpm add -g aws-cdk` |
| `cdk` no se reconoce después de instalarlo con pnpm | El mismo caso anterior: corre `pnpm setup` y reinicia Kiro. Comprueba con `pnpm bin -g` que la carpeta que muestra esté en el PATH |
| `ERR_PNPM_IGNORED_BUILDS` | pnpm bloqueó el script de instalación de un paquete que nadie aprobó; es una protección. Revisa el nombre del paquete en el mensaje y, solo si es una dependencia esperada de AWS CDK, apruébalo con `pnpm add -g aws-cdk --allow-build=<paquete>`. Si no lo reconoces, avisa al facilitador |
| Un error o aviso que menciona `minimumReleaseAge` | pnpm evita por seguridad las versiones publicadas hace menos de 24 horas. Normalmente instala sola la versión anterior; si en tu equipo está configurado en modo estricto, instala una versión que ya cumpla el plazo: `pnpm add -g aws-cdk@<versión-anterior>` (la ves con `pnpm view aws-cdk versions`), o espera un día |
| Windows: `npm install -g pnpm@latest` falla por permisos | No uses PowerShell como administrador. Si persiste, pide a TI que instale pnpm |
| Ya tenías AWS CDK instalado con npm y `cdk --version` muestra otra versión | Desinstala esa copia con `npm uninstall -g aws-cdk` y repite `pnpm add -g aws-cdk` |
