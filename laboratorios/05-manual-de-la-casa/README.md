# Lab 5 · El "manual de la casa" y la memoria

**Módulo 5 · L200 · 20 minutos · Rama de inicio: `lab-05`**

## Qué vas a hacer

Cuando alguien nuevo entra a un equipo, recibe un manual: cómo hablamos con el cliente, qué tecnología usamos, qué no se hace nunca. Kiro tiene lo mismo: el **steering**, archivos en `.kiro/steering/` que el agente lee para trabajar como lo haría alguien de la casa.

Harás un experimento de antes y después: le pedirás un mensaje para el cliente sin steering, agregarás el steering y repetirás el pedido.

Luego activarás la **memoria** de Kiro. El steering lo escribe el equipo **antes** de trabajar; la memoria la va armando Kiro **mientras** trabajas: correcciones que le haces, cosas que descubres al depurar, preferencias tuyas. Kiro las guarda y las recuerda en conversaciones siguientes, sin que se las repitas.

Cada archivo de steering dice **cuándo** se carga:

| Modo | Cuándo lo lee el agente | Ejemplo en este laboratorio |
| --- | --- | --- |
| `always` | Siempre | Producto, tecnología y estructura |
| `fileMatch` | Solo cuando trabaja con ciertos archivos | Estándares de AWS, al tocar `infra/` |
| `auto` | Cuando el pedido coincide con su descripción | Mensajes para el cliente |
| `manual` | Solo cuando lo mencionas con `#` | Guía de diagnóstico |

## Objetivo

Que el agente respete, sin que se lo pidas, el tono con el cliente, la regla de no prometer efectos de salud y los estándares de AWS del proyecto, y que recuerde en una conversación nueva algo que le enseñaste en otra. Al final sabrás cuándo una regla va en steering y cuándo basta con la memoria.

## Antes de empezar

> **Terminal:** abre la terminal de Kiro (**Terminal → New Terminal**) y activa el entorno de Python. Debe aparecer `(.venv)` al inicio de la línea.
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

- **Sigues con tu trabajo:** quédate en tu rama.
- **Te atrasaste:**

```bash
git stash --include-untracked
git switch lab-05
pip install -r requirements-dev.txt
```

## Paso a paso

### Paso 1. Antes: pide un mensaje sin steering

1. Abre una conversación nueva en el chat (botón **+**).
2. Pega:

```text
Redacta el mensaje que ve un cliente en la app cuando su aguacate hass está pintón, e incluye por qué es bueno comerlo.
```

3. Copia la respuesta en un bloc de notas: la compararás al final.

### Paso 2. Genera el steering base

1. En el panel de Kiro, pasa el mouse sobre el título **AGENT STEERING & SKILLS**. A la derecha aparece un **+**: haz clic.
2. En el menú de arriba, elige **Project steering files** (*Automatically create project steering files…*).
3. Espera a que Kiro termine.

**Resultado esperado:** en `.kiro/steering/` aparecen `product.md`, `tech.md` y `structure.md`, escritos por Kiro a partir del proyecto. Ábrelos y léelos.

### Paso 3. Agrega las reglas de la casa

Trae dos archivos de steering ya escritos por el equipo, desde la rama del laboratorio siguiente:

```bash
git restore --source lab-06 .kiro/steering/mensajes-cliente.md .kiro/steering/aws-infra.md .kiro/steering/troubleshooting.md app/frescura/AGENTS.md
```

> Si clonaste el proyecto de GitHub y el comando dice que no encuentra `lab-06`, usa `origin/lab-06`.

Abre cada archivo y fíjate en su encabezado (entre las líneas `---`):

- `mensajes-cliente.md` → `inclusion: auto`: tuteo y nada de "cura", "previene" ni "adelgaza".
- `aws-infra.md` → `inclusion: fileMatch` con `infra/**/*.py`: mínimos privilegios, etiquetas y que el agente nunca despliega.
- `troubleshooting.md` → `inclusion: manual`.
- `app/frescura/AGENTS.md` no tiene encabezado: Kiro lo lee cuando trabaja en esa carpeta.

### Paso 4. Después: repite el pedido

1. Abre una conversación nueva (**+**). El steering se carga al empezar cada conversación.
2. Pega exactamente el mismo pedido del paso 1.
3. Despliega **Included Steering** en la respuesta para ver qué archivos usó.

**Resultado esperado:** el mensaje nuevo usa tuteo, dice cuándo estará listo, incluye "Valores aproximados de referencia" y **no** promete efectos de salud. En **Included Steering** aparece `mensajes-cliente.md`.

### Paso 5. Comprueba el modo fileMatch

1. Abre `infra/stacks/frescura_stack.py`.
2. En el chat:

```text
Si agrego un bucket de S3 nuevo en este archivo, ¿qué estándares debo cumplir?
```

**Resultado esperado:** Kiro cita las reglas de `aws-infra.md`: bucket privado, cifrado, SSL obligatorio, sin nombre fijo y con una prueba en `tests/test_infra.py`.

### Paso 6. Usa el steering manual

```text
#troubleshooting pytest dice que no encuentra el módulo frescura
```

**Resultado esperado:** Kiro responde con el punto 2 de la guía: correr desde la raíz del proyecto con el entorno activo.

### Paso 7. Activa la memoria

> La memoria necesita **Kiro IDE 1.4.0 o posterior**. Si en la barra de actividades de la izquierda no ves el ícono **Memories**, actualiza Kiro (**Help → Check for Updates**) o avisa al facilitador.

1. En la barra de actividades de la izquierda, haz clic en el ícono **Memories**. Se abre la vista de memorias, vacía.
2. Haz clic en el engranaje **Memory settings**. Se abre el ajuste **Kiro Agent: Memory**.
3. Elige **Use and learn**: Kiro usa las memorias y además crea o ajusta memorias nuevas por su cuenta.
4. Kiro muestra un aviso con el botón **Start new session**: haz clic. Si no aparece, abre una conversación nueva con **+**. La memoria aplica solo a conversaciones nuevas.

| Nivel | Qué hace Kiro |
| --- | --- |
| **Use and learn** | Usa las memorias y crea o ajusta memorias por su cuenta |
| **Use but don't learn** | Usa las memorias y solo las cambia cuando se lo pides |
| **Use only** | Usa las memorias existentes, pero nunca las cambia |
| **Off** | No usa ni cambia memorias (es el valor inicial) |

> **Qué no debes pedirle que recuerde:** contraseñas, llaves, datos de clientes ni nada del archivo `.env`. Las memorias se guardan como texto en tu computador.

### Paso 8. Enséñale algo que descubriste trabajando

En el Lab 4 viste que un umbral mal puesto bajó el acierto de etapa por debajo del 85%. Un umbral mal calibrado puede pasar todas las pruebas y aun así equivocarse con fruta real: solo la evaluación lo muestra. Enséñaselo a Kiro. En la conversación nueva, pega:

```text
Algo que aprendimos en este proyecto: cuando se cambie un umbral en app/frescura/datos/catalogo.json, además de pytest hay que correr python eval/evaluar.py y confirmar que el acierto de etapa sigue en 85% o más, porque un umbral mal calibrado puede pasar las pruebas y aun así bajar el acierto. Recuérdalo para este repositorio.
```

**Resultado esperado:** en la respuesta aparece una entrada **Memory created (1)**. Despliégala para ver qué guardó.

Ahora, en la vista **Memories**:

1. Haz clic en **Refresh Memories** (arriba de la vista) si la memoria nueva no aparece.
2. Fíjate en la columna de **ubicación**: dice `analizador-frescura`, es decir, solo aplica a este repositorio. Las memorias **Global** aplican en todos tus proyectos.
3. Haz clic en la memoria. Se abre una pestaña con su **Summary** y su **Content**.

### Paso 9. Compruébalo en una conversación nueva

1. Abre una conversación nueva (**+**). Kiro no ve lo que se habló en la anterior.
2. Pega:

```text
Voy a cambiar el umbral de sobremaduro del mango en el catálogo. ¿Qué debo verificar después del cambio? No modifiques nada todavía.
```

**Resultado esperado:** en la respuesta aparece **Memory accessed (1)** y Kiro te dice que corras `pytest` **y** `python eval/evaluar.py`, y que revises que el acierto de etapa siga en 85% o más. No se lo repetiste: lo recordó.

3. (Opcional) Haz clic en el indicador de uso de contexto, abajo del cuadro del chat. En **Context Usage** aparece una fila **Memory**, después de **Steering files**: lo que Kiro recuerda también ocupa contexto.

### Paso 10. ¿Memoria o steering?

| | Steering | Memoria |
| --- | --- | --- |
| Quién lo escribe | Tú o el equipo, a propósito | Kiro, a partir de lo que pasa en el trabajo |
| Dónde vive | En `.kiro/steering/`, dentro del repositorio | En tu computador, fuera del repositorio |
| Quién lo usa | Todo el que clone el proyecto (viaja con Git) | Solo tú, en Kiro IDE y en Kiro CLI de este computador |
| Cuándo conviene | Reglas que **siempre** deben cumplirse | Contexto que aparece trabajando y que nadie escribiría |

La regla del paso 8 la debería cumplir **todo el equipo**, no solo tú. Por eso, cuando una memoria se vuelve regla, pásala al steering:

```text
Agrega la regla que recordaste sobre los umbrales del catálogo a .kiro/steering/tech.md, en una sección llamada "Cambios de umbrales". Cambia solo ese archivo.
```

**Resultado esperado:** `tech.md` tiene la nueva sección. Desde ahora la regla viaja con el repositorio y la recibe cualquiera que lo clone.

> Para borrar una memoria: en la vista **Memories**, clic derecho sobre ella → **Delete**, y confirma. Hazlo al final del taller si estás en un computador compartido.

### Paso 11. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 5: steering del proyecto y memoria"
```

## Criterio de éxito

- [ ] `.kiro/steering/` tiene `product.md`, `tech.md`, `structure.md`, `mensajes-cliente.md`, `aws-infra.md` y `troubleshooting.md`.
- [ ] El segundo mensaje al cliente usa tuteo y no promete efectos de salud, sin que lo pidieras.
- [ ] Kiro aplicó `aws-infra.md` al hablar de `infra/`.
- [ ] La memoria está en **Use and learn**, y en la vista **Memories** aparece la regla de los umbrales, ubicada en `analizador-frescura`.
- [ ] En una conversación nueva apareció **Memory accessed** y Kiro recordó correr la evaluación.
- [ ] La regla quedó también en `.kiro/steering/tech.md`.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| El segundo mensaje sigue igual | Abriste el chat antes de agregar el steering. Abre una conversación nueva con **+** |
| No aparece **Project steering files** | Escribe en el chat: "Crea los archivos de steering product.md, tech.md y structure.md en .kiro/steering/ a partir de este proyecto" |
| `git restore` dice "pathspec did not match" | Revisa que estás en la raíz del proyecto (`analizador-frescura`) |
| No ves el ícono **Memories** | Tu Kiro es anterior a la 1.4.0. Actualízalo con **Help → Check for Updates** y reinícialo |
| No aparece **Memory created** | Revisa que el nivel sea **Use and learn** y que abriste una conversación **nueva** después de activarlo |
| Aparece **Couldn't save memory** o **Memory not saved** | La carpeta no es de confianza. Paleta de comandos (**Ctrl+Shift+P** o **Cmd+Shift+P**) → **Workspaces: Manage Workspace Trust** → **Trust** y repite el paso 8 |
| En la conversación nueva no aparece **Memory accessed** | Kiro solo trae una memoria cuando el pedido se relaciona con ella. Menciona el catálogo o los umbrales, como en el paso 9 |
| Te quedaste sin tiempo | Cambia a la rama `lab-06`. La memoria no viaja en las ramas: si quieres probarla, haz los pasos 7 a 9 después del taller |

**Para discutir:** ¿qué ha aprendido tu equipo "a las malas" que nadie escribió nunca? ¿Debería quedar en la memoria de cada persona o en el steering del proyecto?
