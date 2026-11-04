# Lab 8 · Agentes especializados y despliegue

**Módulo 8 · L300 · 35 minutos · Rama de inicio: `lab-08`**

## Qué vas a hacer

Un **agente especializado** es un agente con un rol, instrucciones propias y **permisos a la medida** de ese rol. En este laboratorio trabajas con dos, como en un equipo real:

| Agente | Rol | Puede | No puede |
| --- | --- | --- | --- |
| `implementador` | Construye cambios | Escribir en `app/`, `tests/` y `web/`; correr pruebas, lint y evaluación | Tocar `infra/`, `.kiro/` ni `.env`; desplegar; hacer `git push` |
| `revisor-seguridad` | Revisa antes de desplegar | Leer y correr verificaciones | Editar archivos; desplegar |

Vas a **crear el implementador**, usarlo para construir una mejora para el segundo usuario del producto, el **cliente en la app**: un mensaje como "Tu aguacate hass estará en su punto el jueves". Luego el revisor revisa el cambio y **tú despliegas** tu instancia y la pruebas con fotos desde el celular.

## Objetivo

Construir una mejora con un agente de permisos limitados, revisarla con otro agente y tener tu analizador funcionando en AWS.

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

Los dos deben mostrar tu cuenta. Si no, repite los pasos 9 y 10 del [Lab 0](../00-preparacion/README.md). Fija la región del taller (igual en los dos sistemas):

```bash
aws configure set region us-east-1
```

## Paso a paso

### Paso 1. Crea el agente implementador

En el chat de Kiro, en una conversación nueva (**+**), pega:

```text
Crea el archivo .kiro/agents/implementador.json con un agente personalizado de Kiro llamado implementador, usando el formato permissions.rules. Herramientas: read, write y shell. Puede escribir solo en app/, tests/ y web/, y tiene prohibido escribir en infra/, .kiro/, .env y .github/. En la terminal solo puede usar pytest, python -m pytest, python eval/evaluar.py, ruff check, ruff format, git status, git diff y git log, y tiene prohibido cdk deploy, cdk destroy, git push y rm -rf. Carga como contexto el steering del proyecto, app/frescura/AGENTS.md y negocio/. Sus instrucciones: escribir primero las pruebas, implementar el cambio mínimo, correr pytest, ruff check . y python eval/evaluar.py, y entregar una tabla con los archivos que cambió.
```

**Resultado esperado:** Kiro crea `.kiro/agents/implementador.json`.

Compáralo con el de referencia:

```bash
git show lab-09:.kiro/agents/implementador.json
```

Si el tuyo no tiene el bloque `permissions` con reglas `allow` y `deny`, usa el de referencia:

```bash
git restore --source lab-09 .kiro/agents/implementador.json
```

> Si clonaste el proyecto de GitHub y no encuentra `lab-09`, usa `origin/lab-09`.

### Paso 2. Entiende sus permisos

Abre `.kiro/agents/implementador.json` y mira `permissions.rules`:

- `"capability": "fs_write"` controla dónde puede **escribir**; `"capability": "shell"` controla qué **comandos** puede correr.
- `"effect": "allow"` permite y `"effect": "deny"` prohíbe. **Una regla `deny` siempre gana.**
- `resources` es el contexto que carga al empezar: el steering y la política de negocio.

Trae también el agente revisor, que ya está escrito:

```bash
git restore --source lab-09 .kiro/agents/revisor-seguridad.json
```

### Paso 3. Construye la mejora con el implementador

Los agentes personalizados se usan desde Kiro CLI. En la terminal, desde la raíz del proyecto:

```bash
kiro-cli chat --agent implementador
```

Cuando aparezca el cuadro para escribir, pega:

```text
Agrega a la respuesta del análisis el campo mensaje_cliente, para el cliente final, siguiendo .kiro/steering/mensajes-cliente.md. Verde o pintón con 2 o más días: "Tu <producto> estará en su punto el <día de la semana>. Mientras tanto, déjalo a temperatura ambiente." Con 1 día: "Tu <producto> estará en su punto mañana. Mientras tanto, déjalo a temperatura ambiente." Maduro: "Tu <producto> está en su punto. Disfrútalo hoy o mañana." Sobremaduro: "Tu <producto> ya pasó su mejor punto. Aprovéchalo hoy en jugos, batidos o preparaciones." Producto desconocido: null. El producto va en minúscula. El día se calcula con la fecha de Colombia (UTC-5) más dias_hasta_optimo, y esa fecha debe poder fijarse en las pruebas. Inclúyelo en la vista del cliente (app/frescura/vista_cliente.py) y muéstralo en web/cliente.html en un recuadro destacado. Empieza por las pruebas.
```

**Resultado esperado:** en unos 5 a 8 minutos, el agente:

1. Escribe primero las pruebas (por ejemplo `tests/test_mensajes.py`) y comprueba que fallan.
2. Implementa el mensaje (por ejemplo en `app/frescura/mensajes.py`) y lo agrega a la respuesta en `app/frescura/analizador.py`.
3. Lo agrega a la vista del cliente y lo muestra en `web/cliente.html`.
4. Corre `pytest`, `ruff check .` y la evaluación, y entrega la tabla de archivos que cambió.

> **La memoria también está en la CLI.** Kiro IDE y Kiro CLI comparten las memorias del mismo computador. Al terminar, escribe `/memories` en la sesión: verás la regla de los umbrales que le enseñaste en el Lab 5. Si `/memories` pide configurar el acceso, elige **read & write** (aplica desde la siguiente sesión). Si el comando no existe, tu Kiro CLI es anterior a la 2.29.0: este paso es opcional, sigue.

### Paso 4. Comprueba sus límites

En la misma sesión, pega uno por uno:

```text
Agrega la etiqueta Responsable con valor operaciones en infra/app.py.
```

```text
Despliega mi instancia con cdk deploy -c participante=prueba.
```

**Resultado esperado:** las dos acciones quedan **denegadas** por los permisos del agente. El implementador no puede tocar la infraestructura ni desplegar, aunque se lo pidas.

Sal de Kiro CLI con `/quit`.

### Paso 5. Verifica tú mismo

```bash
pytest
ruff check .
```

**Resultado esperado:** ninguna prueba en *failed* (en la referencia, `70 passed`) y `All checks passed!` Abre `web/cliente.html` y busca `mensaje_cliente`.

### Paso 6. Pide la revisión de seguridad

```bash
kiro-cli chat --agent revisor-seguridad
```

Pega:

```text
Revisa la infraestructura y el código antes de desplegar, incluido el cambio del mensaje para el cliente.
```

**Resultado esperado:** una tabla de hallazgos con severidad, archivo:línea y sugerencia, y un veredicto. Es probable que marque que la API no tiene autenticación: está previsto para el piloto. Sal con `/quit`.

### Paso 7. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 8: agentes implementador y revisor, y mensaje para el cliente"
```

### Paso 8. Prepara la cuenta para CDK

```bash
cd infra
cdk bootstrap
```

**Resultado esperado:** termina con `Environment aws://<cuenta>/us-east-1 bootstrapped`. Si el equipo de AWS ya lo hizo, termina en segundos con `(no changes)`.

### Paso 9. Despliega tu instancia

Reemplaza `<tus-iniciales>` por tus iniciales, sin los signos `<` y `>` (por ejemplo `oc`):

```bash
cdk deploy -c participante=<tus-iniciales>
```

1. CDK muestra los permisos que va a crear y pregunta `Do you wish to deploy these changes (y/n)?`. Escribe `y` y presiona **Enter**.
2. Espera unos 5 minutos.

**Resultado esperado:** en **Outputs** aparecen `UrlApi`, `UrlWeb` (vista del personal), `UrlCliente` (vista del cliente), `TablaAnalisis` y `GrupoRegistros`. Cópialos en un bloc de notas.

### Paso 10. Comprueba que la API responde

Reemplaza `<UrlApi>` por tu valor:

Windows (PowerShell):

```powershell
curl.exe <UrlApi>/salud
```

macOS o Linux:

```bash
curl <UrlApi>/salud
```

**Resultado esperado:** `{"estado": "ok"}`.

### Paso 11. Analiza fotos con tu instancia

1. Abre `UrlWeb` en el navegador de tu celular o de tu computador. Puedes enviártela por chat o escribirla.
2. En **Tienda**, escribe `T-<tus-iniciales>`.
3. En **¿No tienes fruta a mano?**, toca una de las fotos de muestra.

**Resultado esperado:** aparecen el producto, la etapa, los días hasta su punto, la confianza, la **acción en tienda**, la nutrición y, al final, la **etapa esperada** de esa foto.

4. Ahora abre `UrlCliente`, la vista del cliente, y toca **la misma** foto de muestra.

**Resultado esperado:** el cliente ve el nombre del producto, una frase como "Está pintón", el **mensaje que construyó el implementador** en un recuadro amarillo ("Tu aguacate hass estará en su punto el jueves…") y la nutrición. **No ve** la acción en tienda ni la confianza. Prueba con varias muestras y compara la etapa que dio el analizador con la esperada: cuando no coinciden, es justo lo que mediría la evaluación del Lab 4 con fotos reales.

> Las fotos de muestra vienen de la colección abierta Fruits-360 (licencia CC BY-SA 4.0; créditos en `web/muestras/CREDITOS.md`). Si tienes una fruta a mano, también puedes tocar **Tomar o elegir foto** y fotografiarla.

### Paso 12. Comprueba el historial

Reemplaza `<TablaAnalisis>` por tu valor:

```bash
aws dynamodb scan --table-name <TablaAnalisis> --select COUNT
```

**Resultado esperado:** `"Count"` igual al número de fotos que analizaste. El historial nunca guarda la foto.

### Paso 13. Vuelve a la raíz del proyecto

```bash
cd ..
```

## Criterio de éxito

- [ ] Existe `.kiro/agents/implementador.json` con permisos `allow` y `deny`.
- [ ] El implementador construyó `mensaje_cliente` con pruebas, y no pudo tocar `infra/` ni desplegar.
- [ ] El revisor entregó su tabla y veredicto sin modificar archivos.
- [ ] `cdk deploy` terminó, la vista del personal muestra la acción en tienda y la del cliente muestra su mensaje sin información interna.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| `kiro-cli chat --agent` no encuentra el agente | Corre el comando desde la raíz del proyecto, donde está `.kiro/agents/` |
| El implementador pide permiso para cada archivo | Revisa que su `permissions` tenga la regla `fs_write` con `allow` para `app/**`, `tests/**` y `web/**`. Si no, usa el de referencia (paso 1) |
| El implementador sí modificó `infra/` | Su archivo no tiene la regla `deny`. Corre `git restore infra/` y usa el agente de referencia |
| Las pruebas del mensaje fallan según el día | El agente no permitió fijar la fecha en las pruebas. Escríbele: "Las pruebas deben pasar cualquier día: recibe la fecha como parámetro y fíjala en las pruebas" |
| `cdk deploy` dice `python: command not found` o "python no se reconoce" | El entorno de Python no está activo en esa terminal. Actívalo y repite dentro de `infra` |
| PowerShell dice "The '<' operator is reserved for future use" | Escribiste los signos `<` y `>`. Usa solo tus iniciales: `cdk deploy -c participante=oc` |
| `cdk deploy` dice "Falta tu identificador" | Agrega `-c participante=<tus-iniciales>` (de 2 a 10 letras o números, empezando con letra) |
| La web dice "No se pudo analizar la imagen" (error 502) | Mira los registros: `aws logs tail <GrupoRegistros> --since 10m`. Si dice `AccessDeniedException`, el modelo de Bedrock no está habilitado en tu cuenta: avisa al equipo de AWS |
| La web dice "Too Many Requests" | Superaste el límite de uso del taller (5 por segundo). Espera unos segundos |
| Te quedaste sin tiempo | Cambia a la rama `lab-09`, que trae los dos agentes y el mensaje para el cliente, y despliega desde ahí |

**Para discutir:** ¿qué ganas al separar quién construye y quién revisa, y al darle a cada uno solo los permisos de su rol?
