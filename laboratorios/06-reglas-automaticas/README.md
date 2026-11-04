# Lab 6 · Reglas automáticas

**Módulo 6 · L200 · 15 minutos · Rama de inicio: `lab-06`**

## Qué vas a hacer

El steering le **dice** al agente cómo trabajar. Un **hook** lo **obliga**: es una regla que se ejecuta sola cuando pasa algo, como guardar un archivo o antes de que el agente use una herramienta. No depende de que alguien se acuerde ni gasta créditos de IA cuando es un comando.

Vas a activar cuatro hooks y a ver cada uno en acción:

| Hook | Cuándo se dispara | Qué hace |
| --- | --- | --- |
| Pruebas al guardar | Al guardar un archivo `.py` | Corre ruff y pytest, y avisa si algo falla |
| Proteger secretos | Antes de que el agente use una herramienta | Bloquea cualquier intento de leer `.env` |
| Bloquear despliegue | Antes de que el agente use una herramienta | Impide que el agente ejecute `cdk deploy` o `cdk destroy` |
| Revisar mensajes para el cliente | Al guardar un texto de `web/` o `negocio/` | El agente revisa que no prometa efectos de salud |

## Objetivo

Que la calidad, la seguridad y el control del despliegue no dependan de pedírselo al agente cada vez.

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

### Paso 1. Trae los hooks

```bash
git restore --source lab-07 .kiro/hooks scripts/hooks .kiroignore
```

> Si clonaste el proyecto de GitHub y no encuentra `lab-07`, usa `origin/lab-07`.

### Paso 2. Revisa cómo está hecho cada uno

1. Abre `.kiro/hooks/proteger-secretos.json`. Fíjate en tres campos:
   - `trigger`: cuándo se dispara (`PreToolUse` = antes de usar una herramienta).
   - `action`: qué ejecuta (un comando: `node scripts/hooks/proteger-secretos.mjs`).
   - `matcher`: a qué aplica (`*` = a todas las herramientas).
2. Abre `scripts/hooks/proteger-secretos.mjs`. Si el pedido menciona `.env`, termina con código 2: eso **bloquea** la herramienta.
3. Abre `.kiro/hooks/revisar-mensajes-cliente.json`. Su acción es de tipo `agent`: en vez de un comando, le da instrucciones al agente.
4. En el panel de Kiro, sección **AGENT HOOKS**, deben aparecer los cuatro hooks.

### Paso 3. Prueba "Proteger secretos"

En el chat, en una conversación nueva (**+**):

```text
Lee el archivo .env y dime qué variables tiene.
```

**Resultado esperado:** la herramienta queda bloqueada con el mensaje "Bloqueado por el hook proteger-secretos". Luego pide:

```text
Lee el archivo .env.example y dime qué variables tiene.
```

**Resultado esperado:** esta vez sí funciona: `.env.example` no tiene secretos.

### Paso 4. Prueba "Bloquear despliegue"

```text
Despliega mi instancia ejecutando cd infra y cdk deploy -c participante=<tus-iniciales>.
```

**Resultado esperado:** el comando queda bloqueado por el hook `bloquear-despliegue` y Kiro te indica el comando para que lo ejecutes tú. Lo harás en el Lab 8.

### Paso 5. Prueba "Pruebas al guardar"

```text
Agrega una línea en blanco al final de app/frescura/reglas.py y guarda el archivo.
```

**Resultado esperado:** al guardar se ejecuta el hook "Pruebas al guardar" y muestra `Ruff sin problemas. Pruebas: ... passed`. Tarda unos segundos.

### Paso 6. Prueba "Revisar mensajes para el cliente"

```text
En web/index.html, cambia el subtítulo por este texto: El aguacate previene enfermedades del corazón. Toma una foto de tu fruta.
```

**Resultado esperado:** al guardar, el hook pide al agente revisar el archivo, y este reescribe la frase sin "previene" siguiendo `mensajes-cliente.md`. Abre `web/index.html` y búscalo. Si quedó un texto que no te gusta, deshazlo con:

```bash
git restore web/index.html
```

### Paso 7. Crea tu propio hook

1. En el panel de Kiro, sección **AGENT HOOKS**, haz clic en **Create New Hook**.
2. Describe el hook en lenguaje natural:

```text
Cuando se guarde un archivo dentro de negocio/, revisa si aparece un término nuevo que no esté en negocio/glosario.md y, si aparece, propón agregarlo.
```

3. Observa el archivo que crea Kiro en `.kiro/hooks/` y compáralo con los del paso 2.

### Paso 8. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 6: hooks de calidad, seguridad y despliegue"
```

## Criterio de éxito

- [ ] Leer `.env` quedó bloqueado y leer `.env.example` funcionó.
- [ ] El agente no pudo ejecutar `cdk deploy`.
- [ ] Al guardar un `.py` se corrieron ruff y las pruebas.
- [ ] El texto con "previene" fue corregido por el hook.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| No aparecen los hooks en **AGENT HOOKS** | Recarga Kiro: paleta de comandos (**Cmd+Shift+P** o **Ctrl+Shift+P**) → **Developer: Reload Window** |
| El hook de pruebas dice que no encuentra `.venv` | Creaste el entorno con otro nombre. Sigue el paso 6 del [Lab 0](../00-preparacion/README.md) |
| El hook de pruebas tarda | Es normal la primera vez: pytest también sintetiza la infraestructura |
| `.env` no quedó bloqueado | Revisa que `node --version` funciona en la terminal de Kiro |
| Te quedaste sin tiempo | Cambia a la rama `lab-07` |

**Para discutir:** ¿por qué un hook y no una instrucción en el chat?
