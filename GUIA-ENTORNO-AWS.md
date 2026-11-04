# Guía del taller en el entorno de AWS

**Workshop de Kiro · Grupo Éxito · Analizador de frescura de frutas y verduras**

Esta guía es para ejecutar todos los laboratorios **en el entorno que entrega AWS el día del taller**: una máquina virtual Linux con Kiro IDE ya instalado, a la que entras desde el navegador o por escritorio remoto. No necesitas instalar nada en tu computador.

> Si vas a trabajar en tu propio computador (Windows, macOS o Linux), usa en cambio las guías de [`laboratorios/`](laboratorios/README.md).

## Contenido

1. [Cómo es el entorno](#1-cómo-es-el-entorno)
2. [Lo que debe estar listo antes del taller](#2-lo-que-debe-estar-listo-antes-del-taller) (equipo de AWS y facilitador)
3. [Convenciones de esta guía](#3-convenciones-de-esta-guía)
4. [Lab 0 · Ingreso al entorno](#lab-0--ingreso-al-entorno) — 10 min
5. [Lab 1 · Primer contacto](#lab-1--primer-contacto) — L100 · 15 min
6. [Lab 2 · De la necesidad al plan](#lab-2--de-la-necesidad-al-plan) — L100 · 25 min
7. [Lab 3 · Construir con el plan](#lab-3--construir-con-el-plan) — L100 · 35 min
8. [Lab 4 · Calidad medible](#lab-4--calidad-medible) — L200 · 15 min
9. [Lab 5 · El "manual de la casa"](#lab-5--el-manual-de-la-casa) — L200 · 15 min
10. [Lab 6 · Reglas automáticas](#lab-6--reglas-automáticas) — L200 · 15 min
11. [Lab 7 · Conectar y estandarizar](#lab-7--conectar-y-estandarizar) — L300 · 20 min
12. [Lab 8 · Agentes especializados y despliegue](#lab-8--agentes-especializados-y-despliegue) — L300 · 35 min
13. [Lab 9 · Orquestar, entregar y cerrar](#lab-9--orquestar-entregar-y-cerrar) — L300 · 25 min
14. [Problemas frecuentes en el entorno de AWS](#problemas-frecuentes-en-el-entorno-de-aws)

---

## 1. Cómo es el entorno

Cada participante recibe su propia cuenta de AWS y su propia máquina virtual. Hay dos formas de entrar, según lo que configure el equipo de AWS:

| Forma de entrar | Qué ves | Cómo entras |
| --- | --- | --- |
| **Kiro IDE en el navegador** | Un escritorio Linux dentro de una pestaña del navegador, con Kiro IDE abierto | Abres la URL que te entregan e ingresas con usuario y contraseña |
| **Máquina virtual con Kiro** | El mismo escritorio Linux, en una ventana de escritorio remoto | Te conectas con los datos que te entregan |

En los dos casos trabajas igual: **Kiro IDE corre en Linux, dentro de AWS**. Eso tiene tres ventajas para el taller:

- Las herramientas ya están instaladas.
- La máquina ya tiene permisos sobre tu cuenta de AWS, a través de un rol. No hay llaves que configurar.
- Todos los participantes tienen el mismo entorno, así que los resultados se parecen.

> **Kiro Web** (app.kiro.dev) es otro producto: trabaja sobre un repositorio de GitHub en una sesión en la nube, sin terminal ni acceso a tu cuenta de AWS. **No sirve para este taller.**

### Lo que hay dentro de la máquina

| Herramienta | Para qué |
| --- | --- |
| Kiro IDE | El entorno de trabajo con el agente de IA |
| Kiro CLI | Los agentes implementador y revisor (Lab 8) y el modo headless (Lab 9) |
| Python 3.12 o superior | El analizador y sus pruebas |
| Node.js 20 o superior y pnpm | AWS CDK y los hooks del Lab 6 |
| AWS CDK | Desplegar la solución |
| AWS CLI | Consultar tu cuenta de AWS |
| Git | Cambiar de laboratorio con las ramas |
| uv | Los servidores MCP del Lab 7 |
| Navegador | Probar tu instancia desplegada |

---

## 2. Lo que debe estar listo antes del taller

**Para el equipo de AWS y el facilitador.** Los participantes pueden saltar esta sección.

### 2.1. Entorno de cada participante

- [ ] Máquina virtual Linux con **Kiro IDE** (la aplicación de escritorio, no solo Kiro CLI), accesible por navegador o escritorio remoto.
- [ ] Herramientas instaladas y en el PATH: Kiro CLI, Python 3.12+, Node.js 20+, pnpm, AWS CDK (`pnpm add -g aws-cdk`), AWS CLI v2, Git y uv.
- [ ] Proyecto `analizador-frescura` con todas sus ramas, ya clonado en `~/analizador-frescura`, o la URL del repositorio para clonarlo.
- [ ] Salida a internet hacia PyPI, el registro de npm, kiro.dev, los servicios de AWS y los paquetes MCP de `awslabs` (uv los descarga en el Lab 7).
- [ ] Copiar y pegar habilitado entre el computador del participante y el escritorio remoto.

### 2.2. Cuenta de AWS de cada participante

- [ ] Región **us-east-1**.
- [ ] Acceso al modelo **Amazon Nova 2 Lite** en Amazon Bedrock, invocado con el perfil de inferencia `us.amazon.nova-2-lite-v1:0`.
- [ ] Rol de la máquina con permisos para `cdk bootstrap` y `cdk deploy`: CloudFormation, IAM (crear roles para la función), Lambda, API Gateway, DynamoDB, S3, CloudFront, CloudWatch Logs, SSM y ECR del bootstrap. La forma más simple en una cuenta de taller es AdministratorAccess.
- [ ] Permiso `pricing:*` para el servidor de precios del Lab 7.
- [ ] `cdk bootstrap` hecho en us-east-1 (opcional: los participantes también pueden hacerlo en el Lab 8).
- [ ] Límite de llamadas a Bedrock suficiente para unos 30 participantes probando al mismo tiempo.

### 2.3. Sesión de Kiro

- [ ] Método de inicio de sesión en Kiro definido (Builder ID o la identidad de la organización) y créditos suficientes por participante. Los Labs 2, 3 y 9 son los que más consumen.
- [ ] Si se hará el modo headless del Lab 9: una **KIRO_API_KEY** para cada participante o solo para el facilitador.

### 2.4. Prueba del facilitador (una cuenta de muestra, antes del taller)

En la máquina de prueba, abre la terminal y ejecuta:

```bash
cd ~/analizador-frescura
git switch final
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
aws sts get-caller-identity
cd infra
cdk deploy -c participante=prueba
```

Resultado esperado: `51 passed`, tu identidad de AWS y, al final del despliegue, las salidas `UrlApi`, `UrlWeb`, `TablaAnalisis` y `GrupoRegistros`. Abre `UrlWeb` en tu celular y analiza una fruta. Después borra todo con `cdk destroy -c participante=prueba`.

---

## 3. Convenciones de esta guía

- **Terminal:** en Kiro, menú **Terminal → New Terminal**. Todos los comandos de esta guía son de Linux (bash).
- **Pegar en la terminal del escritorio remoto:** **Ctrl+Shift+V**. En el chat y en los archivos de Kiro: **Ctrl+V**.
- **Si copiar desde tu computador no funciona,** abre esta misma guía dentro de Kiro: en el explorador, clic derecho sobre `GUIA-ENTORNO-AWS.md` → **Open Preview**. Así copias y pegas dentro del escritorio remoto.
- Los textos en recuadro gris se **copian y pegan tal cual**, en el chat de Kiro o en la terminal, según diga el paso.
- Donde veas `<tus-iniciales>`, escribe tus iniciales en minúscula, sin espacios ni tildes y sin los signos `<` y `>` (por ejemplo `oc`).
- Los nombres de botones y menús aparecen en **negrita**, como se ven en Kiro (en inglés).
- Las respuestas de Kiro cambian de una persona a otra. Lo que importa es el **Resultado esperado** de cada paso.
- **Regla de datos:** los datos de tienda del proyecto son ficticios. No pegues datos reales de clientes, precios ni inventario.

### Si te atrasas: cambiar de rama

Cada rama `lab-NN` tiene el proyecto como debe estar **al empezar** ese laboratorio. Para alcanzar al grupo:

```bash
git stash --include-untracked
git switch lab-05
pip install -r requirements-dev.txt
```

Cambia `lab-05` por la rama que necesites. Tus cambios quedan guardados a un lado, no se pierden.

---

## Lab 0 · Ingreso al entorno

**Al inicio del taller · 10 minutos**

**Qué vas a hacer:** entrar a tu máquina, abrir el proyecto en Kiro y comprobar que todo responde.

### Paso 1. Entra a tu máquina

1. Abre la URL que te entregó el equipo del taller.
2. Ingresa el usuario y la contraseña que te dieron.

**Resultado esperado:** ves un escritorio Linux. Si Kiro no está abierto, ábrelo desde su ícono. Si el ícono está deshabilitado, haz clic derecho sobre él y elige la opción para permitir que se ejecute.

### Paso 2. Inicia sesión en Kiro IDE

Al abrir Kiro por primera vez, inicia sesión con el método que indique el facilitador.

### Paso 3. Abre la terminal y ubica el proyecto

En Kiro, menú **Terminal → New Terminal**.

**Si el proyecto ya está en tu máquina:**

```bash
cd ~/analizador-frescura
```

**Si tienes que clonarlo** (el facilitador te da la URL):

```bash
cd ~
git clone <URL-del-repositorio> analizador-frescura
cd analizador-frescura
for b in lab-01 lab-02 lab-03 lab-04 lab-05 lab-06 lab-07 lab-08 lab-09 final; do git branch --track $b origin/$b 2>/dev/null; done
```

La última línea crea en tu máquina todas las ramas de los laboratorios. Algunos pasos traen archivos de la rama siguiente y las necesitan.

### Paso 4. Abre el proyecto en Kiro

Menú **File → Open Folder**, elige la carpeta `analizador-frescura` (dentro de tu carpeta personal) y confirma. Si Kiro pregunta si confías en los autores, elige confiar.

**Resultado esperado:** en el explorador ves `app`, `infra`, `laboratorios`, `negocio`, `tests`, `web` y este archivo, `GUIA-ENTORNO-AWS.md`.

### Paso 5. Prepara el proyecto

En la terminal de Kiro (abre una nueva con **Terminal → New Terminal**, que ya se ubica en el proyecto):

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.correo@empresa.com"
git switch lab-01
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

**Resultado esperado:** al inicio de la línea aparece `(.venv)` y `pytest` termina con `32 passed, 1 skipped`.

> **Cada vez que abras una terminal nueva, activa el entorno:** `source .venv/bin/activate`

### Paso 6. Comprueba tu cuenta de AWS y Kiro CLI

```bash
aws configure set region us-east-1
aws sts get-caller-identity
kiro-cli login --use-device-flow
```

`kiro-cli login --use-device-flow` muestra una dirección y un código. Ábrela (Ctrl+clic), ingresa el código, autoriza y vuelve a la terminal.

```bash
kiro-cli doctor
```

**Resultado esperado:** `aws sts get-caller-identity` muestra tu cuenta con un rol (`assumed-role`), y `kiro-cli doctor` dice `Everything looks good!`

### Criterio de éxito

- [ ] Kiro abierto con el proyecto.
- [ ] `pytest`: `32 passed, 1 skipped`.
- [ ] Tu cuenta de AWS y Kiro CLI responden.

---

## Lab 1 · Primer contacto

**Módulo 1 · L100 · 15 minutos · Rama: `lab-01`**

### Qué vas a hacer

Conocer el proyecto y trabajar por primera vez con el agente de Kiro: le pedirás que explique el analizador, que muestre dónde se toma cada decisión y que haga un cambio pequeño que luego deshaces.

**El caso:** en la sección de frutas y verduras se pierde producto porque se madura en la góndola sin que nadie actúe a tiempo. El analizador recibe la foto de un banano, aguacate hass, tomate chonto, mango o papaya, y responde su **etapa de madurez** (verde, pintón, maduro o sobremaduro), los **días** que faltan para su punto y su **nutrición** por porción. Un modelo de Amazon Bedrock **describe** la foto; las **reglas del negocio**, en el código, **deciden** la etapa.

### Objetivo

Saber abrir el chat de Kiro, pedirle trabajo, ubicar las secciones de su panel y deshacer un cambio con un *checkpoint*.

### Paso a paso

**Paso 1. Comprueba el proyecto.** En la terminal, con el entorno activo:

```bash
git switch lab-01
pytest
```

Resultado esperado: `32 passed, 1 skipped`.

**Paso 2. Recorre el panel de Kiro.** En la barra de la izquierda, haz clic en el ícono del fantasma de Kiro. Ubica estas secciones:

| Sección | Para qué sirve | Lab |
| --- | --- | --- |
| **SPECS** | Planear una funcionalidad: requisitos, diseño y tareas | 2, 3 y 4 |
| **AGENT HOOKS** | Reglas que se ejecutan solas | 6 |
| **AGENT STEERING & SKILLS** | Contexto de la compañía y procedimientos reutilizables | 5 y 7 |
| **MCP SERVERS** | Conexiones con herramientas externas | 7 |

**Paso 3. Abre el chat.** Está en el panel de la derecha. Para una conversación nueva, haz clic en **+** arriba a la derecha de ese panel. Debajo del cuadro de texto está **Autopilot**: si está activado, Kiro ejecuta comandos y edita archivos sin preguntar; si está desactivado, te pide aprobar cada acción.

**Paso 4. Pide que te explique el proyecto.** Pega en el chat:

```text
Explica en 5 viñetas qué hace este proyecto, cómo viaja una foto desde el celular hasta la respuesta, y qué decide el modelo de IA y qué deciden las reglas del código.
```

Resultado esperado: la foto llega por API Gateway a una función Lambda; Bedrock devuelve producto e índice de madurez; `reglas.py` decide la etapa con los umbrales del catálogo; el historial va a DynamoDB sin la foto.

**Paso 5. Pide un dato con su fuente.**

```text
¿Qué etapa de madurez daría el analizador para un banano con índice 65 y cuántos días faltan para su punto? Dime en qué archivo y en qué función se calcula cada cosa.
```

Resultado esperado: **maduro** y **0 días**, en `app/frescura/reglas.py` (`etapa_madurez` y `dias_hasta_optimo`), con los umbrales del banano en `app/frescura/datos/catalogo.json`.

**Paso 6. Haz un cambio y deshazlo.**

1. Pega:

```text
Agrega un comentario en la primera línea de app/frescura/reglas.py que diga: Prueba del Lab 1.
```

2. Abre `app/frescura/reglas.py` y comprueba el comentario.
3. En el chat, sobre tu último pedido, aparece **Checkpoint** y a la derecha **Restore**. Haz clic en **Restore** y luego en **Confirm**.
4. En la terminal:

```bash
git status --short
```

Resultado esperado: el comentario desapareció y `git status --short` no muestra nada.

**Paso 7. Mira el analizador funcionando.** El facilitador muestra su instancia desplegada analizando una fruta real. En el Lab 8 harás lo mismo con la tuya.

### Criterio de éxito

- [ ] Ubicaste las cuatro secciones del panel.
- [ ] Kiro dio la etapa y los días correctos, citando archivos.
- [ ] Deshiciste un cambio con **Restore**.

---

## Lab 2 · De la necesidad al plan

**Módulo 2 · L100 · 25 minutos · Rama: `lab-02`**

### Qué vas a hacer

El personal de la tienda necesita saber **qué hacer** con cada producto. La compañía tiene una política para eso: `negocio/politica-acciones-tienda.md` (POL-FRV-001). Con Kiro la conviertes en una **spec**, un plan de tres documentos que el agente sigue después para construir:

| Documento | Qué contiene |
| --- | --- |
| `requirements.md` | Qué debe hacer el sistema, en requisitos que se comprueban con sí o no |
| `design.md` | Cómo se va a construir |
| `tasks.md` | La lista de tareas |

**Formato EARS:** cada requisito se escribe como `WHEN <situación> THE <sistema> SHALL <comportamiento>`. Por ejemplo: "WHEN la confianza es menor a 0,70, THE Analizador SHALL recomendar Revisar".

### Objetivo

Una spec completa de la **acción recomendada en tienda**, con requisitos verificables, diseño y como máximo 6 tareas.

### Paso a paso

**Paso 1. Cambia de rama y lee la política.**

```bash
git switch lab-02
```

Abre `negocio/politica-acciones-tienda.md` y lee **3. Reglas, en este orden**: 7 reglas; la primera que se cumple decide la acción.

**Paso 2. Crea la spec.**

1. Panel de Kiro → sección **SPECS** → **Create New Spec**.
2. Arriba se abre un cuadro: *Enter your idea to generate requirement, design, and task specs*. Pega y presiona **Enter**:

```text
Agregar al análisis la acción recomendada en tienda para el personal de frutas y verduras, según la política negocio/politica-acciones-tienda.md (mantener, priorizar, rebajar, transformar, donar, retirar o revisar), con revisión humana cuando la confianza sea menor a 0,70 y sin cambiar la infraestructura.
```

3. En **Input required**, elige **Build a Feature** → **Submit answer**.
4. En *¿Con qué quieres empezar?*, elige **Requirements** → **Submit answer**.
5. Espera de 2 a 3 minutos.

Resultado esperado: tu spec aparece en **SPECS** y Kiro ofrece en el chat **Generar diseño técnico**, **Generar lista de tareas** y **Analizar requerimientos** (pueden aparecer en inglés).

**Paso 3. Revisa los requisitos.** En **SPECS**, abre tu spec → **Requirements**. Comprueba que estén en EARS al menos: confianza menor a 0,70 → Revisar; moho → Retirar; maduro → Priorizar; sobremaduro con 60% o más de manchas → Donar.

**Paso 4. Analiza y decide.**

1. Haz clic en **Analizar requerimientos**. Tarda de 2 a 3 minutos.
2. Haya o no ambigüedades, escribe:

```text
Decisión de negocio: los límites son inclusivos. Confianza de exactamente 0,70 no va a revisión; manchas de exactamente 30% ya es transformar y de exactamente 60% ya es donar. Actualiza los requisitos con esta decisión.
```

**Paso 5. Genera el diseño.** Haz clic en **Generar diseño técnico** (3 a 4 minutos). En **Design**, verifica: el archivo nuevo de reglas (por ejemplo `app/frescura/acciones.py`), el campo `accion` en la respuesta y cómo se prueba cada regla con sus límites.

**Paso 6. Genera las tareas, acotadas.** Escribe en el chat:

```text
Genera la lista de tareas con máximo 6 tareas. Las pruebas son obligatorias, no opcionales: no marques ninguna tarea con asterisco.
```

Resultado esperado: `tasks.md` con 6 tareas o menos, ninguna con `*`.

**Paso 7. Guarda tu trabajo.**

```bash
git add -A
git commit -m "Lab 2: spec de la acción en tienda"
```

### Criterio de éxito

- [ ] Existen `requirements.md`, `design.md` y `tasks.md` en `.kiro/specs/<tu-spec>/`.
- [ ] Las 7 reglas están en EARS, con límites explícitos.
- [ ] `tasks.md` tiene 6 tareas o menos y las pruebas son obligatorias.

**Si te atrasaste:** cambia a la rama `lab-03`, que trae una spec de referencia.

---

## Lab 3 · Construir con el plan

**Módulo 3 · L100 · 35 minutos · Rama: `lab-03`**

### Qué vas a hacer

Pedirle a Kiro que **ejecute las tareas** de la spec: escribe el código de la acción en tienda y sus pruebas, mientras tú observas y verificas. Tú defines **qué** y con qué reglas; el agente resuelve **cómo**.

### Objetivo

Que el analizador responda la acción recomendada en tienda, con pruebas que la respalden.

### Paso a paso

**Paso 1. Abre la lista de tareas.** Si te atrasaste, primero cambia a `lab-03`. En **SPECS**, abre tu spec → **Tasks**.

**Paso 2. Pide la ejecución en el chat.**

```text
Ejecuta todas las tareas de tasks.md de la spec de acción en tienda, incluidas las pruebas. Al terminar, corre pytest y ruff check . y dime el resultado.
```

> **No uses** el comando de la paleta *Execute all incomplete required tasks in the spec*: en la versión probada da el error `makeAllRequired` y omite las tareas opcionales.

Resultado esperado: Kiro trabaja en modo orquestador y explica qué corre en paralelo. Tarda unos 10 a 15 minutos.

**Paso 3. Observa el avance.** En `tasks.md`, cada tarea pasa a *Task in progress* y luego a *Task completed*. En el chat, despliega **N tool calls** para ver qué archivos toca.

**Paso 4. Verifica tú mismo.**

```bash
pytest
ruff check .
```

Resultado esperado: más pruebas que las 32 originales, ninguna en *failed*, 1 *skipped* (en la referencia: `46 passed, 1 skipped`), y `All checks passed!`

**Paso 5. Comprueba la política con casos.**

```text
Sin cambiar archivos, dime qué acción recomienda el código para estos casos y en qué línea se decide cada uno: (1) mango sobremaduro con 40% de manchas, (2) banano maduro con confianza 0,65, (3) papaya verde con moho, (4) aguacate hass sobremaduro con 60% de manchas.
```

| Caso | Acción esperada |
| --- | --- |
| 1 | Transformar, con el mensaje "jugos o pulpa" |
| 2 | Revisar |
| 3 | Retirar |
| 4 | Donar, con confirmación del jefe |

**Paso 6. Guarda tu trabajo.**

```bash
git add -A
git commit -m "Lab 3: acción en tienda"
```

### Criterio de éxito

- [ ] Todas las tareas completas.
- [ ] `pytest` sin *failed* y con más pruebas que al inicio.
- [ ] Los 4 casos dan la acción correcta.

**Si te atrasaste:** cambia a la rama `lab-04`.

---

## Lab 4 · Calidad medible

**Módulo 4 · L200 · 15 minutos · Rama: `lab-04`**

### Qué vas a hacer

El acierto del analizador hay que **medirlo**. El proyecto trae una evaluación con 60 fotos etiquetadas (3 por producto y etapa). La meta del piloto es **85%** y hoy no se cumple por un error en el código. Lo encuentras, lo corriges con una **Bugfix Spec** y lo blindas con **pruebas basadas en propiedades**.

> En el taller, la evaluación usa lecturas de ejemplo que simulan lo que respondería el modelo. Así todos obtienen el mismo resultado sin costo.

### Objetivo

Subir el acierto de etapa del 83,3% al 88,3% sin romper nada.

### Paso a paso

**Paso 1. Prepara la rama.**

- **Sigues con tu trabajo:** abre `tests/test_reglas.py`, borra la línea `@pytest.mark.skip(reason="Se activa en el Lab 4")` y guarda.
- **Te atrasaste:** cambia a `lab-04` (ahí la prueba ya está activa).

**Paso 2. Mide el acierto.**

```bash
python eval/evaluar.py
```

Resultado esperado: `Acierto de etapa: 83.3% (mínimo 85%)`. En `eval/reporte.md`, sección **Confusiones de etapa**, hay fotos sobremaduras leídas como maduras.

**Paso 3. Confirma el error.**

```bash
pytest
```

Resultado esperado: `1 failed`, en `test_umbral_exacto_de_sobremaduro_ya_es_sobremaduro`: un banano con índice exactamente 80 sale `maduro`.

**Paso 4. Crea la Bugfix Spec.**

1. **SPECS** → **Create New Spec**. Pega y presiona **Enter**:

```text
Un producto con índice de madurez exactamente igual a su umbral de sobremaduro se clasifica como maduro. Ejemplo: banano con índice 80 da maduro y debería dar sobremaduro. Lo muestran tests/test_reglas.py y eval/evaluar.py, que baja al 83,3% de acierto.
```

2. En **Input required**, elige **Fix a Bug** → **Submit answer**. Si Kiro pregunta algo más, responde con la información de la descripción.

Resultado esperado: `bugfix.md` con el comportamiento actual, el esperado y lo que no debe cambiar.

**Paso 5. Ejecuta la corrección.**

```text
Ejecuta las tareas de la spec del bug. Al terminar corre pytest y python eval/evaluar.py y dime los resultados.
```

Resultado esperado: `pytest` sin *failed* y `Acierto de etapa: 88.3% (mínimo 85%)`. El cambio es un carácter: `>` por `>=` en `app/frescura/reglas.py`.

**Paso 6. Pruebas basadas en propiedades.**

```text
Crea tests/test_propiedades.py con pruebas basadas en propiedades usando Hypothesis para todos los productos del catálogo: (1) la etapa nunca retrocede si el índice aumenta, (2) un índice igual a cada umbral pertenece a la etapa que ese umbral inicia, (3) si está maduro o sobremaduro faltan 0 días y si no, al menos 1, (4) el doble de gramos da el doble de energía, con tolerancia de 0,2. Córrelas con pytest.
```

Resultado esperado: 4 pruebas nuevas que pasan. La propiedad (2) habría detectado el error desde el principio.

**Paso 7. Guarda tu trabajo.**

```bash
git add -A
git commit -m "Lab 4: corrige el umbral y agrega pruebas de propiedades"
```

### Criterio de éxito

- [ ] La evaluación cumple el mínimo: 88,3%.
- [ ] `pytest` sin *failed*.
- [ ] `tests/test_propiedades.py` con 4 propiedades que pasan.

**Si te atrasaste:** cambia a la rama `lab-05`.

---

## Lab 5 · El "manual de la casa"

**Módulo 5 · L200 · 15 minutos · Rama: `lab-05`**

### Qué vas a hacer

El **steering** es el manual de la casa para el agente: archivos en `.kiro/steering/` que lee para trabajar como alguien del equipo. Harás un experimento de antes y después.

| Modo | Cuándo lo lee el agente | Ejemplo |
| --- | --- | --- |
| `always` | Siempre | Producto, tecnología y estructura |
| `fileMatch` | Al trabajar con ciertos archivos | Estándares de AWS, al tocar `infra/` |
| `auto` | Cuando el pedido coincide con su descripción | Mensajes para el cliente |
| `manual` | Solo cuando lo mencionas con `#` | Guía de diagnóstico |

### Objetivo

Que el agente respete, sin pedírselo, el tono con el cliente, la regla de no prometer efectos de salud y los estándares de AWS.

### Paso a paso

**Paso 1. Antes: un mensaje sin steering.** Conversación nueva (**+**) y pega:

```text
Redacta el mensaje que ve un cliente en la app cuando su aguacate hass está pintón, e incluye por qué es bueno comerlo.
```

Copia la respuesta en un archivo de notas para compararla al final.

**Paso 2. Genera el steering base.**

1. En el panel de Kiro, pasa el mouse sobre **AGENT STEERING & SKILLS** y haz clic en el **+** que aparece.
2. Elige **Project steering files**.
3. Espera a que termine.

Resultado esperado: `product.md`, `tech.md` y `structure.md` en `.kiro/steering/`.

**Paso 3. Agrega las reglas de la casa.**

```bash
git restore --source lab-06 .kiro/steering/mensajes-cliente.md .kiro/steering/aws-infra.md .kiro/steering/troubleshooting.md app/frescura/AGENTS.md
```

Abre cada archivo y mira su encabezado entre las líneas `---`: `mensajes-cliente.md` es `auto` (tuteo y nada de "cura", "previene" ni "adelgaza"); `aws-infra.md` es `fileMatch` con `infra/**/*.py`; `troubleshooting.md` es `manual`; `app/frescura/AGENTS.md` aplica a esa carpeta.

**Paso 4. Después: repite el pedido.** Conversación nueva (**+**), pega el mismo texto del paso 1 y despliega **Included Steering** en la respuesta.

Resultado esperado: tuteo, cuándo estará listo, "Valores aproximados de referencia" y ninguna promesa de salud. En **Included Steering** aparece `mensajes-cliente.md`.

**Paso 5. Modo fileMatch.** Abre `infra/stacks/frescura_stack.py` y pregunta:

```text
Si agrego un bucket de S3 nuevo en este archivo, ¿qué estándares debo cumplir?
```

Resultado esperado: bucket privado, cifrado, SSL obligatorio, sin nombre fijo y una prueba en `tests/test_infra.py`.

**Paso 6. Modo manual.**

```text
#troubleshooting pytest dice que no encuentra el módulo frescura
```

Resultado esperado: correr desde la raíz del proyecto con el entorno activo.

**Paso 7. Guarda tu trabajo.**

```bash
git add -A
git commit -m "Lab 5: steering del proyecto"
```

### Criterio de éxito

- [ ] Seis archivos en `.kiro/steering/`.
- [ ] El segundo mensaje usa tuteo y no promete salud, sin pedirlo.
- [ ] Kiro aplicó `aws-infra.md` al hablar de `infra/`.

**Si te atrasaste:** cambia a la rama `lab-06`.

---

## Lab 6 · Reglas automáticas

**Módulo 6 · L200 · 15 minutos · Rama: `lab-06`**

### Qué vas a hacer

Un **hook** es una regla que se ejecuta sola cuando pasa algo: al guardar un archivo o antes de que el agente use una herramienta. El steering **le dice** al agente cómo trabajar; el hook **lo obliga**.

| Hook | Cuándo | Qué hace |
| --- | --- | --- |
| Pruebas al guardar | Al guardar un `.py` | Corre ruff y pytest |
| Proteger secretos | Antes de usar una herramienta | Bloquea leer `.env` |
| Bloquear despliegue | Antes de usar una herramienta | Impide al agente `cdk deploy` y `cdk destroy` |
| Revisar mensajes para el cliente | Al guardar un texto de `web/` o `negocio/` | El agente quita promesas de salud |

### Objetivo

Que la calidad, la seguridad y el control del despliegue no dependan de pedírselo al agente.

### Paso a paso

**Paso 1. Trae los hooks.**

```bash
git restore --source lab-07 .kiro/hooks scripts/hooks .kiroignore
```

**Paso 2. Revisa cómo están hechos.** Abre `.kiro/hooks/proteger-secretos.json`: `trigger` (cuándo), `matcher` (a qué aplica) y `action` (qué ejecuta). Abre `scripts/hooks/proteger-secretos.mjs`: si el pedido menciona `.env`, termina con código 2 y eso bloquea la herramienta. En el panel, **AGENT HOOKS** debe listar los cuatro hooks.

**Paso 3. Proteger secretos.** Conversación nueva (**+**):

```text
Lee el archivo .env y dime qué variables tiene.
```

Resultado esperado: bloqueado por `proteger-secretos`. Luego:

```text
Lee el archivo .env.example y dime qué variables tiene.
```

Resultado esperado: funciona.

**Paso 4. Bloquear despliegue.**

```text
Despliega mi instancia ejecutando cd infra y cdk deploy -c participante=<tus-iniciales>.
```

Resultado esperado: bloqueado por `bloquear-despliegue`; Kiro te indica el comando para que lo ejecutes tú en el Lab 8.

**Paso 5. Pruebas al guardar.**

```text
Agrega una línea en blanco al final de app/frescura/reglas.py y guarda el archivo.
```

Resultado esperado: se ejecuta "Pruebas al guardar" y muestra `Ruff sin problemas. Pruebas: ... passed`.

**Paso 6. Revisar mensajes para el cliente.**

```text
En web/index.html, cambia el subtítulo por este texto: El aguacate previene enfermedades del corazón. Toma una foto de tu fruta.
```

Resultado esperado: al guardar, el hook hace que el agente reescriba la frase sin "previene". Si no te gusta cómo quedó: `git restore web/index.html`.

**Paso 7. Crea tu propio hook.** **AGENT HOOKS** → **Create New Hook**, y describe:

```text
Cuando se guarde un archivo dentro de negocio/, revisa si aparece un término nuevo que no esté en negocio/glosario.md y, si aparece, propón agregarlo.
```

Compara el archivo que crea Kiro en `.kiro/hooks/` con los del paso 2.

**Paso 8. Guarda tu trabajo.**

```bash
git add -A
git commit -m "Lab 6: hooks de calidad, seguridad y despliegue"
```

### Criterio de éxito

- [ ] `.env` bloqueado y `.env.example` permitido.
- [ ] El agente no pudo desplegar.
- [ ] Al guardar un `.py` corrieron ruff y las pruebas.
- [ ] El hook corrigió el texto con "previene".

**Si te atrasaste:** cambia a la rama `lab-07`.

---

## Lab 7 · Conectar y estandarizar

**Módulo 7 · L300 · 20 minutos · Rama: `lab-07`**

### Qué vas a hacer

Darle al agente dos capacidades: **MCP**, para conectarlo con herramientas externas (aquí, la **documentación** y los **precios** oficiales de AWS), y **skills**, procedimientos del equipo empaquetados para reutilizar (la **ficha de un producto** y la **estimación de costo del piloto**).

### Objetivo

Consultar documentación y precios reales de AWS desde Kiro y producir dos entregables con skills.

### Paso a paso

**Paso 1. Trae la configuración y las skills.**

```bash
git restore --source lab-08 .kiro/settings/mcp.json .kiro/settings/mcp.windows.json .kiro/skills
```

En este entorno (Linux) se usa `mcp.json` tal como viene. `mcp.windows.json` es para quien trabaje en Windows.

**Paso 2. Revisa la configuración.** Abre `.kiro/settings/mcp.json`: `aws-docs` (documentación, sin credenciales) y `aws-pricing` (precios, con las credenciales de tu máquina).

**Paso 3. Comprueba la conexión.** En **MCP SERVERS**, `aws-docs` y `aws-pricing` deben aparecer como **Connected**. La primera vez tardan hasta un minuto.

**Paso 4. Consulta la documentación.** Conversación nueva (**+**):

```text
Usando la documentación oficial de AWS, ¿cuál es el tamaño máximo del cuerpo de una invocación síncrona de AWS Lambda? Relaciónalo con el límite de 4 MB que valida app/frescura/handler.py y con que la web reduzca la foto a 1024 px.
```

Resultado esperado: **6 MB**, citando la documentación de AWS; la imagen en base64 crece cerca de un tercio, por eso el límite de 4 MB y la reducción de la foto.

**Paso 5. Skill de ficha de producto.** Lee `.kiro/skills/ficha-producto/SKILL.md` y pide:

```text
Dame la ficha del mango.
```

Resultado esperado: umbrales 25, 55 y 85; 10 puntos por día; **6 días** desde verde hasta su punto; destino "jugos o pulpa"; 60 kcal, 1,6 g de fibra, 168 mg de potasio y 36,4 mg de vitamina C por 100 g; un mensaje para el cliente sin promesas de salud.

**Paso 6. Estima el costo del piloto.**

```text
Estima el costo mensual del piloto con 5 tiendas y 200 fotos por tienda al día.
```

Resultado esperado: Kiro usa la skill `estimar-costo-piloto`, consulta precios con `aws-pricing` y crea `docs/costo-piloto.md` con supuestos, costo por servicio con fórmula, total mensual y costo por foto.

**Paso 7. Guarda tu trabajo.**

```bash
git add -A
git commit -m "Lab 7: MCP de AWS, skills y estimación de costo"
```

### Criterio de éxito

- [ ] `aws-docs` y `aws-pricing` conectados.
- [ ] La respuesta sobre Lambda cita la documentación de AWS.
- [ ] La ficha del mango usa los datos del proyecto.
- [ ] Existe `docs/costo-piloto.md` con precios consultados.

**Si te atrasaste:** cambia a la rama `lab-08`.

---

## Lab 8 · Agentes especializados y despliegue

**Módulo 8 · L300 · 35 minutos · Rama: `lab-08`**

Antes de empezar, comprueba tu cuenta y Kiro CLI:

```bash
aws sts get-caller-identity
kiro-cli whoami
```

### Qué vas a hacer

Un **agente especializado** es un agente con un rol, instrucciones propias y **permisos a la medida** de ese rol. En este laboratorio trabajas con dos, como en un equipo real:

| Agente | Rol | Puede | No puede |
| --- | --- | --- | --- |
| `implementador` | Construye cambios | Escribir en `app/`, `tests/` y `web/`; correr pruebas, lint y evaluación | Tocar `infra/`, `.kiro/` ni `.env`; desplegar; hacer `git push` |
| `revisor-seguridad` | Revisa antes de desplegar | Leer y correr verificaciones | Editar archivos; desplegar |

Vas a **crear el implementador**, usarlo para construir una mejora para el segundo usuario del producto, el **cliente en la app**: un mensaje como "Tu aguacate hass estará en su punto el jueves". Luego el revisor revisa el cambio y **tú despliegas** tu instancia y la pruebas con una fruta real desde el celular.

### Objetivo

Construir una mejora con un agente de permisos limitados, revisarla con otro agente y tener tu analizador funcionando en AWS.

### Paso a paso

#### Paso 1. Crea el agente implementador

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

#### Paso 2. Entiende sus permisos

Abre `.kiro/agents/implementador.json` y mira `permissions.rules`:

- `"capability": "fs_write"` controla dónde puede **escribir**; `"capability": "shell"` controla qué **comandos** puede correr.
- `"effect": "allow"` permite y `"effect": "deny"` prohíbe. **Una regla `deny` siempre gana.**
- `resources` es el contexto que carga al empezar: el steering y la política de negocio.

Trae también el agente revisor, que ya está escrito:

```bash
git restore --source lab-09 .kiro/agents/revisor-seguridad.json
```

#### Paso 3. Construye la mejora con el implementador

Los agentes personalizados se usan desde Kiro CLI. En la terminal, desde la raíz del proyecto:

```bash
kiro-cli chat --agent implementador
```

Cuando aparezca el cuadro para escribir, pega:

```text
Agrega a la respuesta del análisis el campo mensaje_cliente, para el cliente final, siguiendo .kiro/steering/mensajes-cliente.md. Verde o pintón con 2 o más días: "Tu <producto> estará en su punto el <día de la semana>. Mientras tanto, déjalo a temperatura ambiente." Con 1 día: "Tu <producto> estará en su punto mañana. Mientras tanto, déjalo a temperatura ambiente." Maduro: "Tu <producto> está en su punto. Disfrútalo hoy o mañana." Sobremaduro: "Tu <producto> ya pasó su mejor punto. Aprovéchalo hoy en jugos, batidos o preparaciones." Producto desconocido: null. El producto va en minúscula. El día se calcula con la fecha de Colombia (UTC-5) más dias_hasta_optimo, y esa fecha debe poder fijarse en las pruebas. Muestra el mensaje en web/index.html. Empieza por las pruebas.
```

**Resultado esperado:** en unos 5 a 8 minutos, el agente:

1. Escribe primero las pruebas (por ejemplo `tests/test_mensajes.py`) y comprueba que fallan.
2. Implementa el mensaje (por ejemplo en `app/frescura/mensajes.py`) y lo agrega a la respuesta en `app/frescura/analizador.py`.
3. Lo muestra en `web/index.html`.
4. Corre `pytest`, `ruff check .` y la evaluación, y entrega la tabla de archivos que cambió.

#### Paso 4. Comprueba sus límites

En la misma sesión, pega uno por uno:

```text
Agrega la etiqueta Responsable con valor operaciones en infra/app.py.
```

```text
Despliega mi instancia con cdk deploy -c participante=prueba.
```

**Resultado esperado:** las dos acciones quedan **denegadas** por los permisos del agente. El implementador no puede tocar la infraestructura ni desplegar, aunque se lo pidas.

Sal de Kiro CLI con `/quit`.

#### Paso 5. Verifica tú mismo

```bash
pytest
ruff check .
```

**Resultado esperado:** ninguna prueba en *failed* (en la referencia, `61 passed`) y `All checks passed!` Abre `web/index.html` y busca `mensaje_cliente`.

#### Paso 6. Pide la revisión de seguridad

```bash
kiro-cli chat --agent revisor-seguridad
```

Pega:

```text
Revisa la infraestructura y el código antes de desplegar, incluido el cambio del mensaje para el cliente.
```

**Resultado esperado:** una tabla de hallazgos con severidad, archivo:línea y sugerencia, y un veredicto. Es probable que marque que la API no tiene autenticación: está previsto para el piloto. Sal con `/quit`.

#### Paso 7. Guarda tu trabajo

```bash
git add -A
git commit -m "Lab 8: agentes implementador y revisor, y mensaje para el cliente"
```

#### Paso 8. Prepara la cuenta para CDK

```bash
cd infra
cdk bootstrap
```

**Resultado esperado:** termina con `Environment aws://<cuenta>/us-east-1 bootstrapped`. Si el equipo de AWS ya lo hizo, termina en segundos con `(no changes)`.

#### Paso 9. Despliega tu instancia

Reemplaza `<tus-iniciales>` por tus iniciales, sin los signos `<` y `>` (por ejemplo `oc`):

```bash
cdk deploy -c participante=<tus-iniciales>
```

1. CDK muestra los permisos que va a crear y pregunta `Do you wish to deploy these changes (y/n)?`. Escribe `y` y presiona **Enter**.
2. Espera unos 5 minutos.

**Resultado esperado:** en **Outputs** aparecen `UrlApi`, `UrlWeb`, `TablaAnalisis` y `GrupoRegistros`. Cópialos a un archivo de notas.

#### Paso 10. Comprueba que la API responde

Reemplaza `<UrlApi>` por tu valor:

```bash
curl <UrlApi>/salud
```

**Resultado esperado:** `{"estado": "ok"}`.

#### Paso 11. Analiza una fruta real

1. Abre `UrlWeb` en el navegador de **tu celular**. La URL es pública: puedes escribirla, enviártela por chat o generar un código QR.
2. En **Tienda**, escribe `T-<tus-iniciales>`.
3. Toca **Tomar o elegir foto** y fotografía de cerca una fruta de la mesa, con buena luz y una sola fruta en la foto.

**Resultado esperado:** aparecen el producto, la etapa, los días hasta su punto, la confianza, la **acción en tienda**, la nutrición y, al final, **Para el cliente:** con el mensaje que construyó el implementador. Prueba con frutas en distintas etapas.

#### Paso 12. Comprueba el historial

Reemplaza `<TablaAnalisis>` por tu valor:

```bash
aws dynamodb scan --table-name <TablaAnalisis> --select COUNT
```

**Resultado esperado:** `"Count"` igual al número de fotos que analizaste. El historial nunca guarda la foto.

#### Paso 13. Vuelve a la raíz del proyecto

```bash
cd ..
```

### Criterio de éxito

- [ ] Existe `.kiro/agents/implementador.json` con permisos `allow` y `deny`.
- [ ] El implementador construyó `mensaje_cliente` con pruebas, y no pudo tocar `infra/` ni desplegar.
- [ ] El revisor entregó su tabla y veredicto sin modificar archivos.
- [ ] `cdk deploy` terminó y en el celular aparece el mensaje para el cliente.

**Si te atrasaste:** cambia a la rama `lab-09`, que trae los dos agentes y el mensaje para el cliente, y despliega desde ahí.

---

## Lab 9 · Orquestar, entregar y cerrar

**Módulo 9 · L300 · 25 minutos · Rama: `lab-09`**

### Qué vas a hacer

1. **Delegar una investigación** con un **workflow**: Kiro coordina varios pasos en segundo plano y entrega un informe de riesgos para llevar el analizador a 50 tiendas.
2. **Llevar los controles al flujo de entrega:** revisar la integración continua y ejecutar Kiro CLI en modo **headless**, como lo haría ese pipeline.
3. **Dejar la hoja de ruta** del piloto y **borrar tu instancia**.

### Objetivo

Salir con el informe de riesgos, la hoja de ruta del piloto completa y tu cuenta limpia.

### Paso a paso

**Paso 1. Lanza el workflow.** Conversación nueva (**+**):

```text
Usa un workflow para investigar, sin modificar ningún archivo, qué riesgos técnicos, operativos y de costo tiene llevar el analizador de frescura a 50 tiendas. Usa el código, la infraestructura, eval/reporte.md, docs/costo-piloto.md y los documentos de negocio/. Cita archivos, propone una mitigación para cada riesgo y guarda el informe en .kiro/reports/piloto.md.
```

Resultado esperado: el botón **Workflows**, arriba del chat, muestra un workflow en curso. Sigue con el paso 2 mientras corre.

> Si te falta `eval/reporte.md`, corre `python eval/evaluar.py`. Si te falta `docs/costo-piloto.md`, el informe será menos concreto en costos.

**Paso 2. Revisa la integración continua.**

```bash
git restore --source final .github/workflows/ci.yml
```

Abre `.github/workflows/ci.yml`. En cada *pull request* corre: `ruff check .`, `pytest`, `python eval/evaluar.py --minimo 85`, `cdk synth` y el agente `revisor-seguridad` en headless. Corre tú los cuatro primeros:

```bash
ruff check .
pytest
python eval/evaluar.py --minimo 85
cd infra
cdk synth -c participante=ci -q
cd ..
```

Resultado esperado: los cuatro terminan sin error.

**Paso 3. Revisor en modo headless.** Si el facilitador te entregó una **KIRO_API_KEY**:

```bash
export KIRO_API_KEY=<tu-api-key>
kiro-cli chat --v3 --no-interactive --agent revisor-seguridad --trust-tools=read_file,grep_search "Revisa los cambios del último commit y entrega tu tabla de hallazgos y el veredicto"
```

Resultado esperado: la tabla y el veredicto aparecen sin que respondas nada. Sin API key, mira la demostración del facilitador.

**Paso 4. Revisa el informe.** Abre `.kiro/reports/piloto.md`: riesgos técnicos, operativos y de costo, con archivo de referencia y mitigación. Por ejemplo: la API no tiene autenticación, las fotos de evaluación son de ejemplo y el límite de llamadas a Bedrock con 50 tiendas.

**Paso 5. Completa la hoja de ruta.**

```bash
git restore --source final negocio/hoja-de-ruta-piloto.md
```

```text
Completa la sección "Dónde estamos" de negocio/hoja-de-ruta-piloto.md con los datos de eval/reporte.md, docs/costo-piloto.md y .kiro/reports/piloto.md. No inventes datos: si falta alguno, déjalo en blanco. Deja vacías las columnas de responsable y fecha.
```

Completa tú la URL de tu instancia y el próximo paso.

**Paso 6. Guarda tu trabajo.**

```bash
git add -A
git commit -m "Lab 9: informe de riesgos, CI y hoja de ruta del piloto"
```

**Paso 7. Borra tu instancia.**

```bash
cd infra
cdk destroy -c participante=<tus-iniciales>
```

Cuando pregunte `Are you sure you want to delete: Frescura-<tus-iniciales> (y/n)?`, escribe `y`. Resultado esperado: `Frescura-<tus-iniciales>: destroyed`.

> Si vas a conservar tu trabajo, antes de que cierren el entorno sube tu rama a un repositorio propio o descarga la carpeta del proyecto. El equipo de AWS elimina las cuentas y máquinas del taller al terminar.

### Criterio de éxito

- [ ] `.kiro/reports/piloto.md` con riesgos y mitigaciones.
- [ ] Los cuatro controles del pipeline pasan.
- [ ] Hoja de ruta con tus números y un próximo paso.
- [ ] Instancia borrada.

---

## Problemas frecuentes en el entorno de AWS

| Síntoma | Qué hacer |
| --- | --- |
| No puedo pegar en la terminal | Usa **Ctrl+Shift+V**. Si tampoco funciona, abre esta guía dentro de Kiro (**Open Preview**) y copia desde ahí |
| El ícono de Kiro está deshabilitado | Clic derecho sobre el ícono y elige la opción para permitir que se ejecute |
| `pytest` dice "No module named frescura" o "No module named hypothesis" | Activa el entorno (`source .venv/bin/activate`) y corre `pip install -r requirements-dev.txt` desde la raíz del proyecto |
| `git restore --source lab-06 …` dice que no encuentra la rama | Clonaste el proyecto sin crear las ramas locales. Corre la línea `for b in …` del paso 3 del Lab 0 |
| `git commit` dice "Please tell me who you are" | Corre los dos `git config --global` del paso 5 del Lab 0 |
| `kiro-cli login` no avanza | Usa `kiro-cli login --use-device-flow` |
| `aws sts get-caller-identity` falla | La máquina no tiene el rol de AWS asignado. Avisa al equipo de AWS |
| `cdk deploy` dice `python: command not found` | Activa el entorno de Python en esa terminal y repite dentro de `infra` |
| `cdk deploy` falla con `AccessDenied` | El rol de la máquina no tiene permisos suficientes para desplegar. Avisa al equipo de AWS |
| La web dice "No se pudo analizar la imagen" (502) | Mira los registros: `aws logs tail <GrupoRegistros> --since 10m`. Si dice `AccessDeniedException`, Bedrock no está habilitado en tu cuenta: avisa al equipo de AWS |
| La web dice "Too Many Requests" | Superaste el límite de uso del taller (5 por segundo). Espera unos segundos |
| Un servidor MCP no conecta | Revisa `uv --version` y los registros en **View → Output → Kiro - MCP Logs** |
| `aws-pricing` da error de permisos | El rol necesita `pricing:*`. Avisa al equipo de AWS |
| Kiro responde en inglés | Escribe: "Responde en español de aquí en adelante" |
| Te atrasaste en cualquier laboratorio | Cambia a la rama del laboratorio siguiente (ver [Si te atrasas](#si-te-atrasas-cambiar-de-rama)) |
