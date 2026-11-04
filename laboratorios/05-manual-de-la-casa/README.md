# Lab 5 · El "manual de la casa"

**Módulo 5 · L200 · 15 minutos · Rama de inicio: `lab-05`**

## Qué vas a hacer

Cuando alguien nuevo entra a un equipo, recibe un manual: cómo hablamos con el cliente, qué tecnología usamos, qué no se hace nunca. Kiro tiene lo mismo: el **steering**, archivos en `.kiro/steering/` que el agente lee para trabajar como lo haría alguien de la casa.

Harás un experimento de antes y después: le pedirás un mensaje para el cliente sin steering, agregarás el steering y repetirás el pedido.

Cada archivo de steering dice **cuándo** se carga:

| Modo | Cuándo lo lee el agente | Ejemplo en este laboratorio |
| --- | --- | --- |
| `always` | Siempre | Producto, tecnología y estructura |
| `fileMatch` | Solo cuando trabaja con ciertos archivos | Estándares de AWS, al tocar `infra/` |
| `auto` | Cuando el pedido coincide con su descripción | Mensajes para el cliente |
| `manual` | Solo cuando lo mencionas con `#` | Guía de diagnóstico |

## Objetivo

Que el agente respete, sin que se lo pidas, el tono con el cliente, la regla de no prometer efectos de salud y los estándares de AWS del proyecto.

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

### Paso 7. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 5: steering del proyecto"
```

## Criterio de éxito

- [ ] `.kiro/steering/` tiene `product.md`, `tech.md`, `structure.md`, `mensajes-cliente.md`, `aws-infra.md` y `troubleshooting.md`.
- [ ] El segundo mensaje al cliente usa tuteo y no promete efectos de salud, sin que lo pidieras.
- [ ] Kiro aplicó `aws-infra.md` al hablar de `infra/`.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| El segundo mensaje sigue igual | Abriste el chat antes de agregar el steering. Abre una conversación nueva con **+** |
| No aparece **Project steering files** | Escribe en el chat: "Crea los archivos de steering product.md, tech.md y structure.md en .kiro/steering/ a partir de este proyecto" |
| `git restore` dice "pathspec did not match" | Revisa que estás en la raíz del proyecto (`analizador-frescura`) |
| Te quedaste sin tiempo | Cambia a la rama `lab-06` |
