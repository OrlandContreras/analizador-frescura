# Lab 3 · Construir con el plan

**Módulo 3 · L100 · 35 minutos · Rama de inicio: `lab-03`**

## Qué vas a hacer

Con la spec del Lab 2 lista, le pides a Kiro que **ejecute las tareas**. El agente escribe el código de la acción en tienda y sus pruebas, tarea por tarea, mientras tú observas y verificas.

Este es el cambio de fondo de trabajar con agentes: tú defines **qué** se construye y con qué reglas (la spec), y el agente se encarga de **cómo**. Después compruebas que el resultado cumple lo pedido.

## Objetivo

Que el analizador responda la acción recomendada en tienda, con pruebas que la respalden.

## Antes de empezar

Elige una opción:

- **Sigues con tu spec del Lab 2:** quédate en tu rama actual.
- **Te atrasaste:** cambia a `lab-03`, que trae una spec de referencia en `.kiro/specs/accion-en-tienda/`:

```bash
git stash --include-untracked
git switch lab-03
pip install -r requirements-dev.txt
```

## Paso a paso

### Paso 1. Abre la lista de tareas

En el panel de Kiro, sección **SPECS**, haz clic en tu spec y luego en **Tasks**. Lee las tareas: es lo que el agente va a hacer.

### Paso 2. Pide la ejecución en el chat

En el chat, pega:

```text
Ejecuta todas las tareas de tasks.md de la spec de acción en tienda, incluidas las pruebas. Al terminar, corre pytest y ruff check . y dime el resultado.
```

> **No uses** el comando de la paleta *Execute all incomplete required tasks in the spec*: en la versión probada da un error (`makeAllRequired`) y además omite las tareas opcionales.

**Resultado esperado:** Kiro trabaja en modo orquestador. Explica qué tareas corre en paralelo y cuáles en secuencia porque tocan el mismo archivo. Tarda unos 10 a 15 minutos.

### Paso 3. Observa el avance

Mientras trabaja, abre `tasks.md`. Cada tarea pasa a *Task in progress* y luego a *Task completed*. En el chat, despliega **N tool calls** para ver qué archivos lee y escribe.

### Paso 4. Verifica tú mismo

Cuando Kiro termine, en la terminal:

```bash
pytest
ruff check .
```

**Resultado esperado:**

- `pytest`: más pruebas que las 32 originales, **ninguna en *failed*** y 1 *skipped* (la del Lab 4). En la solución de referencia salen `46 passed, 1 skipped`; tu número puede ser distinto.
- `ruff check .`: `All checks passed!`

### Paso 5. Comprueba las reglas con casos de la política

Pega en el chat:

```text
Sin cambiar archivos, dime qué acción recomienda el código para estos casos y en qué línea se decide cada uno: (1) mango sobremaduro con 40% de manchas, (2) banano maduro con confianza 0,65, (3) papaya verde con moho, (4) aguacate hass sobremaduro con 60% de manchas.
```

**Resultado esperado:**

| Caso | Acción |
| --- | --- |
| 1 | Transformar, con el mensaje "jugos o pulpa" |
| 2 | Revisar (confianza menor a 0,70) |
| 3 | Retirar (el moho va antes que la etapa) |
| 4 | Donar, con confirmación del jefe |

Si algún caso no coincide, pide a Kiro que lo corrija y agregue la prueba que falta.

### Paso 6. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 3: acción en tienda"
```

## Criterio de éxito

- [ ] Todas las tareas de `tasks.md` están completas.
- [ ] `pytest` sin pruebas en *failed* y con más pruebas que al inicio.
- [ ] Los 4 casos del paso 5 dan la acción correcta.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| Una tarea falla | Escribe: "Corrige el error de la tarea N y vuelve a ejecutarla" |
| Aparece el error `makeAllRequired` | Usaste la paleta de comandos. Cierra el aviso y pide la ejecución en el chat, como en el paso 2 |
| Kiro modificó la infraestructura | Escribe: "La spec dice que no se cambia la infraestructura. Revierte los cambios en infra/" |
| Te quedaste sin tiempo | Cambia a la rama `lab-04`: trae la acción en tienda ya implementada |
