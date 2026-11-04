# Lab 4 · Calidad medible

**Módulo 4 · L200 · 15 minutos · Rama de inicio: `lab-04`**

## Qué vas a hacer

Un analizador que va a decidir qué se rebaja o se dona en una tienda no puede funcionar "más o menos": su acierto hay que **medirlo**. El proyecto trae una evaluación con 60 fotos etiquetadas (3 por producto y por etapa) que compara la etapa que da el analizador con la etapa real.

La meta del piloto es **85% de acierto**. Hoy no se cumple, por un error en el código. Lo vas a encontrar, corregir con una **Bugfix Spec** y blindar con **pruebas basadas en propiedades**, que prueban cientos de casos generados automáticamente.

> En el taller, la evaluación usa lecturas de ejemplo (`eval/lecturas_ejemplo.json`) que simulan lo que respondería el modelo para cada foto. Así todos obtienen el mismo resultado y no hay costo. En el piloto se mide con fotos reales y el modelo real (`--modo bedrock`).

## Objetivo

Subir el acierto de etapa del 83,3% al 88,3%, sin romper nada de lo que funciona, y dejar pruebas que impidan que el error vuelva.

## Antes de empezar

> **Terminal:** abre la terminal de Kiro (**Terminal → New Terminal**) y activa el entorno de Python. Debe aparecer `(.venv)` al inicio de la línea.
> - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
> - macOS o Linux: `source .venv/bin/activate`

Elige una opción:

- **Sigues con tu trabajo del Lab 3:** quédate en tu rama y activa la prueba del error. Abre `tests/test_reglas.py`, borra la línea `@pytest.mark.skip(reason="Se activa en el Lab 4")` y guarda.
- **Te atrasaste:** cambia a `lab-04`, donde la prueba ya está activa:

```bash
git stash --include-untracked
git switch lab-04
pip install -r requirements-dev.txt
```

## Paso a paso

### Paso 1. Mide el acierto

```bash
python eval/evaluar.py
```

**Resultado esperado:**

```
Acierto de producto: 96.7%
Acierto de etapa:    83.3% (mínimo 85%)
```

Abre `eval/reporte.md`. En **Confusiones de etapa** aparecen fotos **sobremaduras** leídas como **maduras**.

### Paso 2. Confirma el error con la prueba

```bash
pytest
```

**Resultado esperado:** `1 failed`. La que falla es `test_umbral_exacto_de_sobremaduro_ya_es_sobremaduro`: un banano con índice exactamente 80 (su umbral de sobremaduro) sale como `maduro`.

### Paso 3. Crea una Bugfix Spec

1. En el panel de Kiro, sección **SPECS**, haz clic en **Create New Spec**.
2. Pega esta descripción y presiona **Enter**:

```text
Un producto con índice de madurez exactamente igual a su umbral de sobremaduro se clasifica como maduro. Ejemplo: banano con índice 80 da maduro y debería dar sobremaduro. Lo muestran tests/test_reglas.py y eval/evaluar.py, que baja al 83,3% de acierto.
```

3. En **Input required**, elige **Fix a Bug** y haz clic en **Submit answer**.
4. Si Kiro hace más preguntas, respóndelas con la información de la descripción.

**Resultado esperado:** una spec con `bugfix.md` que separa tres cosas: el comportamiento actual (el error), el esperado y lo que **no debe cambiar**.

### Paso 4. Ejecuta la corrección

En el chat:

```text
Ejecuta las tareas de la spec del bug. Al terminar corre pytest y python eval/evaluar.py y dime los resultados.
```

**Resultado esperado:**

- `pytest`: ninguna prueba en *failed*.
- `python eval/evaluar.py`: `Acierto de etapa: 88.3% (mínimo 85%)`.

El cambio real es de un solo carácter: `>` por `>=` en `app/frescura/reglas.py`. Ábrelo y búscalo.

### Paso 5. Blinda las reglas con pruebas basadas en propiedades

En el chat:

```text
Crea tests/test_propiedades.py con pruebas basadas en propiedades usando Hypothesis para todos los productos del catálogo: (1) la etapa nunca retrocede si el índice aumenta, (2) un índice igual a cada umbral pertenece a la etapa que ese umbral inicia, (3) si está maduro o sobremaduro faltan 0 días y si no, al menos 1, (4) el doble de gramos da el doble de energía, con tolerancia de 0,2, (5) para cualquier lectura, la vista del cliente nunca incluye accion ni lectura, y reconocido es falso si el producto es desconocido o la confianza es menor a 0,70. Córrelas con pytest.
```

**Resultado esperado:** 5 pruebas nuevas que pasan. La propiedad (2) es la que habría detectado el error desde el principio, y la (5) protege al cliente: ningún cambio futuro podrá mostrarle información interna sin que falle una prueba.

### Paso 6. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 4: corrige el umbral de sobremaduro y agrega pruebas de propiedades"
```

## Criterio de éxito

- [ ] `python eval/evaluar.py` cumple el mínimo: 88,3%.
- [ ] `pytest` sin pruebas en *failed*.
- [ ] Existe `tests/test_propiedades.py` con 4 propiedades que pasan.

## Si algo no sale

| Síntoma | Qué hacer |
| --- | --- |
| `pytest` dice "No module named hypothesis" | Corre `pip install -r requirements-dev.txt` con el entorno activo |
| El acierto no llega a 88,3% | Revisa que el cambio fue solo en el umbral de sobremaduro. Pide: "Muéstrame el diff de app/frescura/reglas.py" |
| Kiro cambió los umbrales del catálogo | Escribe: "No cambies catalogo.json; el error está en la comparación de reglas.py". Luego corre `git restore app/frescura/datos/catalogo.json` |
| Te quedaste sin tiempo | Cambia a la rama `lab-05` |

**Para discutir:** ¿por qué medir con fotos etiquetadas antes de llevar el analizador a una tienda?
