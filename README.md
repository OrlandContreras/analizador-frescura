# Analizador de frescura de frutas y verduras

> **Proyecto de práctica del workshop de Kiro.** Los datos de tienda, las cifras de negocio y las políticas son ficticios. Los valores nutricionales son de referencia (USDA FoodData Central) y deben validarse con la tabla del ICBF antes de un piloto.

Con una foto tomada desde el celular, el analizador identifica el producto, estima su etapa de madurez y los días que faltan para su punto óptimo, y entrega su información nutricional por porción. Tiene dos vistas que se construyen a la par: la del **personal de tienda** (`web/index.html`), que en el taller recibe la **acción recomendada en tienda** según la política `negocio/politica-acciones-tienda.md`, y la del **cliente comprador** (`web/cliente.html`), que solo ve información pública: cuándo estará en su punto lo que compró y su nutrición.

## Arquitectura

```
Celular ──► CloudFront + S3 (web/index.html: personal · web/cliente.html: cliente)
   │
   └──► API Gateway (HTTP API) ──► Lambda (Python 3.12, app/frescura)
                                      ├─► Amazon Bedrock (visión: producto e índice de madurez)
                                      ├─► Reglas de madurez y catálogo (app/frescura/reglas.py)
                                      └─► DynamoDB (historial de análisis, sin imágenes)
```

El modelo **describe** lo que ve; las **reglas del negocio deciden** la etapa y la acción. Así cada recomendación se puede auditar y los umbrales se ajustan sin cambiar de modelo.

## Estructura

```
app/frescura/        Código de la función: visión, reglas, nutrición, historial y handler
app/frescura/datos/  Catálogo de 5 productos con sus umbrales y tabla de nutrición
infra/               Infraestructura con AWS CDK (Python): un stack por participante
web/                 Vistas del personal (index.html) y del cliente (cliente.html), estilos y fotos de muestra
tests/               Pruebas con pytest (sin llamar a AWS)
eval/                Evaluación del acierto con fotos etiquetadas
negocio/             Necesidad, política de acciones en tienda y glosario
scripts/             Analizar una foto desde tu computador con Bedrock
```

## Prerrequisitos para el workshop

> **¿Vas a trabajar en el entorno que entrega AWS** (Kiro IDE en el navegador o en una máquina virtual)? Usa la guía [GUIA-ENTORNO-AWS.md](GUIA-ENTORNO-AWS.md): ahí no instalas nada y tiene todos los laboratorios paso a paso. Lo que sigue es para trabajar en tu propio computador.

Antes del taller, sigue la guía [Lab 0 · Preparación del equipo](laboratorios/00-preparacion/README.md). Instala y comprueba todo esto:

| Herramienta | Versión | Para qué |
| --- | --- | --- |
| Kiro IDE | Última | Entorno de trabajo con el agente de IA |
| Kiro CLI | Última | Agentes implementador y revisor, y modo headless (Labs 8 y 9) |
| Python | 3.12 o superior | El analizador y sus pruebas |
| Node.js | 20 o superior | AWS CDK y los hooks del Lab 6 |
| pnpm | 12 o superior | Instalar AWS CDK con controles de seguridad (no se usa npm) |
| AWS CDK | 2.x, instalado con `pnpm add -g aws-cdk` | Desplegar la solución |
| AWS CLI | 2.x | Conectar con tu cuenta de AWS |
| Git | Cualquiera reciente | Cambiar de laboratorio con las ramas |
| uv | Última | Servidores MCP del Lab 7 |

El día del taller, el equipo de AWS entrega a cada participante una cuenta en la región **us-east-1** con acceso al modelo **Amazon Nova 2 Lite** en Amazon Bedrock.

Si `pnpm add -g aws-cdk` falla, la tabla **Problemas con pnpm** del [Lab 0](laboratorios/00-preparacion/README.md#problemas-con-pnpm) explica cómo resolver cada error.

## Preparar el proyecto

Windows (PowerShell, la terminal por defecto de Kiro en Windows):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest
```

macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

Con el entorno activo (`(.venv)` al inicio de la línea), el resto de los comandos de este README son iguales en Windows y en macOS o Linux.

Resultado esperado en `main`: `33 passed, 1 skipped`. La prueba omitida es intencional: se activa en el Lab 4.

## Medir el acierto

```bash
python eval/evaluar.py
```

Usa lecturas de ejemplo (sin costo) y escribe `eval/reporte.md`. Con las fotos en `eval/fotos/`, `python eval/evaluar.py --modo bedrock` mide el modelo real.

## Desplegar tu instancia

Cada participante despliega su propia copia. Reemplaza `oc` por tus iniciales (de 2 a 10 letras o números, empezando con letra). La región del taller se fija una vez con `aws configure set region us-east-1`:

```bash
cd infra
cdk bootstrap        # solo la primera vez en la cuenta y región, si el equipo del taller no lo hizo
cdk deploy -c participante=oc
```

Al terminar, CDK muestra `UrlWeb` (vista del personal), `UrlCliente` (vista del cliente) y `UrlApi`. Ábrelas en el celular.

Para usar otro modelo de Bedrock: `cdk deploy -c participante=oc -c modeloVision=<id del perfil de inferencia>`.

## Borrar tu instancia al final del taller

```bash
cd infra
cdk destroy -c participante=oc
```

## API

| Método | Ruta | Qué hace |
| --- | --- | --- |
| GET | `/salud` | Comprueba que la API responde |
| GET | `/productos` | Lista los productos que reconoce |
| POST | `/analisis` | Analiza una foto. Cuerpo: `{"imagen_base64": "...", "gramos": 150, "tienda": "T-001"}` |

Los errores responden `{"error": {"code", "message"}}`. La foto debe ser JPEG o PNG de hasta 4 MB; la web la reduce a 1024 px antes de enviarla.

## Laboratorios y ramas

Las guías del taller están en [`laboratorios/`](laboratorios/README.md), una carpeta por laboratorio con su `README.md`.

Cada rama tiene el proyecto **al inicio** de un laboratorio. Si te atrasas, cambia a la rama del laboratorio siguiente:

```bash
git stash --include-untracked
git switch lab-05
pip install -r requirements-dev.txt
```

| Rama | Estado del proyecto |
| --- | --- |
| `main`, `lab-01` y `lab-02` | Proyecto base |
| `lab-03` | + spec de la acción en tienda (Lab 2) |
| `lab-04` | + acción en tienda implementada (Lab 3) y la prueba del error activa |
| `lab-05` | + error corregido y pruebas de propiedades (Lab 4) |
| `lab-06` | + steering, con la regla de cambios de umbrales que nace de la memoria (Lab 5) |
| `lab-07` | + hooks (Lab 6) |
| `lab-08` | + MCP de AWS y skills (Lab 7) |
| `lab-09` | + agentes implementador y revisor de seguridad, mensaje para el cliente (Lab 8), y el Power `operacion-frescura` ya creado |
| `lab-10` | + resumen de uso de ejemplo en `docs/uso-piloto.md` (Lab 9), workflow `investigar-piloto` y plantilla de la hoja de ruta |
| `final` | + workflow `preparar-piloto`, integración continua (Lab 10) |
