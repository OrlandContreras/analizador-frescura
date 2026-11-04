# Lab 6 · Reglas automáticas

**Módulo 6 · L200 · 15 minutos · Rama de inicio: `lab-06`**

## Qué vas a hacer

El steering le **dice** al agente cómo trabajar. Un **hook** lo **obliga**: es una regla que se ejecuta sola cuando pasa algo, como guardar un archivo o antes de que el agente use una herramienta. No depende de que alguien se acuerde, y cuando ejecuta un comando no gasta créditos de IA.

Vas a trabajar con cuatro hooks. Tres ya están escritos: los traes, los lees y los pruebas. **El cuarto lo creas tú**, paso a paso.

| Hook | Cuándo se dispara | Qué hace | Quién lo hace |
| --- | --- | --- | --- |
| Pruebas al guardar | Al guardar un archivo `.py` | Corre ruff y pytest, y avisa si algo falla | Ya está escrito |
| Proteger secretos | Antes de que el agente use una herramienta | Bloquea cualquier intento de leer `.env` | Ya está escrito |
| Bloquear despliegue | Antes de que el agente use una herramienta | Impide que el agente ejecute `cdk deploy` o `cdk destroy` | Ya está escrito |
| **Revisar mensajes para el cliente** | Al guardar un texto de `web/` o `negocio/` | Le pide al agente revisar que el texto no prometa efectos de salud | **Lo creas tú** |

## Objetivo

Entender cómo está hecho un hook, crear uno propio y comprobar que la calidad, la seguridad y el control del despliegue ya no dependen de pedírselo al agente.

## Antes de empezar

> **Terminal:** abre la terminal de Kiro (**Terminal → New Terminal**) y activa el entorno de Python. Debe aparecer `(.venv)` al inicio de la línea.
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

- **Sigues con tu trabajo:** quédate en tu rama.
- **Te atrasaste:**

```bash
git stash --include-untracked
git switch lab-06
pip install -r requirements-dev.txt
```

## Paso a paso

### Paso 1. Trae los tres hooks ya escritos

```bash
git restore --source lab-07 .kiro/hooks/pruebas-al-guardar.json .kiro/hooks/proteger-secretos.json .kiro/hooks/bloquear-despliegue.json scripts/hooks .kiroignore
```

> Si clonaste el proyecto de GitHub y no encuentra `lab-07`, usa `origin/lab-07`.

**Resultado esperado:** aparece la carpeta `.kiro/hooks/` con tres archivos `.json`, y la carpeta `scripts/hooks/` con los programas que ejecutan.

### Paso 2. Entiende cómo está hecho un hook

Abre `.kiro/hooks/proteger-secretos.json`. Todo hook tiene la misma estructura:

```json
{
  "version": "v1",
  "hooks": [
    {
      "name": "Proteger secretos",
      "description": "Lab 6: impide que el agente lea o use el archivo .env.",
      "trigger": "PreToolUse",
      "matcher": "*",
      "action": { "type": "command", "command": "node scripts/hooks/proteger-secretos.mjs" },
      "timeout": 10
    }
  ]
}
```

| Campo | Qué significa |
| --- | --- |
| `version` | Versión del formato. Siempre `"v1"` |
| `hooks` | Lista de hooks del archivo, entre corchetes `[ ]` |
| `name` | Nombre que ves en el panel de Kiro |
| `description` | Para qué sirve, en una frase |
| `trigger` | **Cuándo** se dispara. `PreToolUse` = antes de que el agente use una herramienta; `PostFileSave` = después de guardar un archivo |
| `matcher` | **A qué** aplica. `"*"` = a todo; también puede ser un patrón que debe aparecer en la ruta del archivo |
| `action` | **Qué** hace. `"type": "command"` ejecuta un programa; `"type": "agent"` le da una instrucción al agente |
| `timeout` | Segundos máximos que puede tardar un comando |

Ahora abre `scripts/hooks/proteger-secretos.mjs`: si el pedido menciona `.env`, el programa termina con código 2 y eso **bloquea** la herramienta.

### Paso 3. Prueba "Proteger secretos"

En el chat, en una conversación nueva (**+**):

```text
Lee el archivo .env y dime qué variables tiene.
```

**Resultado esperado:** la herramienta queda bloqueada con el mensaje "Bloqueado por el hook proteger-secretos". Luego:

```text
Lee el archivo .env.example y dime qué variables tiene.
```

**Resultado esperado:** esta vez funciona, porque `.env.example` no tiene secretos.

### Paso 4. Prueba "Bloquear despliegue"

```text
Despliega mi instancia ejecutando cd infra y cdk deploy -c participante=prueba.
```

**Resultado esperado:** el comando queda bloqueado por `bloquear-despliegue` y Kiro te indica el comando para que lo ejecutes tú. Lo harás en el Lab 8.

### Paso 5. Prueba "Pruebas al guardar"

```text
Agrega una línea en blanco al final de app/frescura/reglas.py y guarda el archivo.
```

**Resultado esperado:** al guardar se ejecuta "Pruebas al guardar" y muestra `Ruff sin problemas. Pruebas: ... passed`. Tarda unos segundos.

### Paso 6. Crea tu propio hook: "Revisar mensajes para el cliente"

Este hook se dispara **cada vez que se guarda** un archivo de `web/` o `negocio/` (`PostFileSave`) y, en lugar de ejecutar un programa, **le da una instrucción al agente** (`"type": "agent"`): revisar que el texto no prometa efectos de salud.

**6.1. Crea el archivo vacío.**

1. En la barra de la izquierda, abre el **Explorer** (el ícono de las hojas, arriba de todo).
2. Despliega la carpeta `.kiro` y luego `hooks`.
3. Haz clic derecho sobre la carpeta `hooks` y elige **New File…**
4. Escribe el nombre `revisar-mensajes-cliente.json` y presiona **Enter**.

**Resultado esperado:** se abre un archivo vacío llamado `revisar-mensajes-cliente.json` dentro de `.kiro/hooks/`.

**6.2. Escribe el hook.** Copia y pega este contenido en el archivo vacío:

```json
{
  "version": "v1",
  "hooks": [
    {
      "name": "Revisar mensajes para el cliente",
      "description": "Lab 6: cuando se guarda un texto de la web o de negocio, el agente revisa que no prometa efectos de salud.",
      "trigger": "PostFileSave",
      "matcher": "(web|negocio).*(html|md)$",
      "action": {
        "type": "agent",
        "prompt": "Revisa el archivo que se acaba de guardar. Si algún texto dirigido al cliente promete efectos de salud (cura, previene, sana, adelgaza, quema grasa, desintoxica, garantiza), reescribe solo esa frase siguiendo .kiro/steering/mensajes-cliente.md y explica el cambio en una línea. Si no hay nada que corregir, responde solo: Sin cambios."
      }
    }
  ]
}
```

**6.3. Lee lo que acabas de escribir.** Compáralo con la tabla del paso 2:

| Campo | Valor en tu hook | Por qué |
| --- | --- | --- |
| `trigger` | `"PostFileSave"` | Se revisa el texto **después** de guardarlo |
| `matcher` | `"(web\|negocio).*(html\|md)$"` | Solo archivos de `web/` o `negocio/` que terminen en `html` o `md`. Los `.py` no lo disparan |
| `action.type` | `"agent"` | No ejecuta un programa: le da una instrucción al agente |
| `action.prompt` | La instrucción | Qué debe revisar y cómo corregirlo, siguiendo el steering del Lab 5 |

**6.4. Guarda el archivo** con **Ctrl+S** (Windows o Linux) o **Cmd+S** (macOS).

**6.5. Comprueba que el JSON es válido.** En la terminal:

```bash
python -m json.tool .kiro/hooks/revisar-mensajes-cliente.json
```

**Resultado esperado:** se imprime el contenido ordenado, sin errores. Si aparece `Expecting ',' delimiter` o un error parecido, falta o sobra una coma o una comilla en la línea que indica: compara con el contenido del paso 6.2.

**6.6. Comprueba que Kiro lo reconoce.** Abre el panel de Kiro (ícono del fantasma). En **AGENT HOOKS** deben aparecer los cuatro hooks, incluido **Revisar mensajes para el cliente**.

**6.7. Pruébalo.** En el chat:

```text
En web/index.html, cambia el subtítulo por este texto: El aguacate previene enfermedades del corazón. Toma una foto de tu fruta.
```

**Resultado esperado:** el agente guarda `web/index.html`, tu hook se dispara y el agente reescribe la frase **sin "previene"**, explicando el cambio en una línea. Abre `web/index.html` y busca el subtítulo.

**6.8. Ajústalo.** Agrega una palabra prohibida más:

1. En `revisar-mensajes-cliente.json`, dentro de `prompt`, cambia `garantiza)` por `garantiza, milagroso)`.
2. Guarda con **Ctrl+S** o **Cmd+S**.
3. Prueba otra vez:

```text
En web/index.html, cambia el subtítulo por este texto: Un mango milagroso para tu día. Toma una foto de tu fruta.
```

**Resultado esperado:** el hook corrige "milagroso". Para dejar la página como estaba:

```bash
git restore web/index.html
```

### Paso 7 (opcional). Crea un hook describiéndolo en lenguaje natural

También puedes pedirle a Kiro que escriba el hook por ti:

1. En el panel de Kiro, sección **AGENT HOOKS**, haz clic en **Create New Hook**.
2. Describe el hook:

```text
Cuando se guarde un archivo dentro de negocio/, revisa si aparece un término nuevo que no esté en negocio/glosario.md y, si aparece, propón agregarlo.
```

3. Abre el archivo que crea Kiro en `.kiro/hooks/` y compáralo con el que escribiste en el paso 6: ¿qué `trigger`, `matcher` y `action` eligió?

### Paso 8. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 6: hooks de calidad, seguridad, despliegue y mensajes"
```

## Criterio de éxito

- [ ] Leer `.env` quedó bloqueado y leer `.env.example` funcionó.
- [ ] El agente no pudo ejecutar `cdk deploy`.
- [ ] Al guardar un `.py` se corrieron ruff y las pruebas.
- [ ] **Creaste** `.kiro/hooks/revisar-mensajes-cliente.json`, aparece en **AGENT HOOKS** y corrigió las frases con "previene" y "milagroso".

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| No aparecen los hooks en **AGENT HOOKS** | Recarga Kiro: paleta de comandos (**Ctrl+Shift+P** o **Cmd+Shift+P**) → **Developer: Reload Window** |
| Tu hook no aparece pero los otros sí | El JSON tiene un error. Corre el comando del paso 6.5 y corrige la línea que indica |
| No ves la carpeta `.kiro` en el Explorer | Revisa que abriste la carpeta `analizador-frescura` (**File → Open Folder**). Si sigue sin verse, créala desde la terminal con el paso 1 |
| Tu hook no se dispara al cambiar `web/index.html` | Revisa que `trigger` sea exactamente `PostFileSave` y que el `matcher` sea `(web\|negocio).*(html\|md)$` |
| El hook de pruebas dice que no encuentra `.venv` | Creaste el entorno con otro nombre. Sigue el paso 7 del [Lab 0](../00-preparacion/README.md) |
| `.env` no quedó bloqueado | Revisa que `node --version` funciona en la terminal de Kiro |
| Te quedaste sin tiempo | Cambia a la rama `lab-07`, que trae los cuatro hooks |

**Para discutir:** ¿por qué un hook y no una instrucción en el chat? ¿Cuándo conviene un hook de tipo `command` y cuándo uno de tipo `agent`?
