# Analizador de frescura de frutas y verduras

> **Proyecto de práctica del workshop de Kiro con Grupo Éxito.** Los datos de tienda, las cifras de negocio y las políticas son ficticios. Los valores nutricionales son de referencia (USDA FoodData Central) y deben validarse con la tabla del ICBF antes de un piloto.

Con una foto tomada desde el celular, el analizador identifica el producto, estima su etapa de madurez y los días que faltan para su punto óptimo, y entrega su información nutricional por porción. En el taller se le agrega la **acción recomendada en tienda** según la política `negocio/politica-acciones-tienda.md`.

## Arquitectura

```
Celular ──► CloudFront + S3 (web/index.html)
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
web/                 Página web móvil para tomar la foto
tests/               Pruebas con pytest (sin llamar a AWS)
eval/                Evaluación del acierto con fotos etiquetadas
negocio/             Necesidad, política de acciones en tienda y glosario
scripts/             Analizar una foto desde tu computador con Bedrock
```

## Requisitos

- Python 3.12 o superior
- Node.js 20 o superior y el CLI de AWS CDK: `npm install -g aws-cdk`
- AWS CLI configurado con la cuenta del taller, en la región **us-east-1**
- Acceso al modelo **Amazon Nova 2 Lite** en Amazon Bedrock (lo habilita el equipo del taller)

## Preparar el proyecto

macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest
```

Resultado esperado en `main`: `32 passed, 1 skipped`. La prueba omitida es intencional: se activa en el Lab 4.

## Medir el acierto

```bash
python eval/evaluar.py
```

Usa lecturas de ejemplo (sin costo) y escribe `eval/reporte.md`. Con las fotos en `eval/fotos/`, `python eval/evaluar.py --modo bedrock` mide el modelo real.

## Desplegar tu instancia

Cada participante despliega su propia copia. Reemplaza `oc` por tus iniciales (de 2 a 10 letras o números, empezando con letra):

```bash
cd infra
cdk bootstrap        # solo la primera vez en la cuenta y región, si el equipo del taller no lo hizo
cdk deploy -c participante=oc
```

Al terminar, CDK muestra `UrlWeb` (ábrela en el celular) y `UrlApi`.

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
| `lab-06` | + steering (Lab 5) |
| `lab-07` | + hooks (Lab 6) |
| `lab-08` | + MCP de AWS y skills (Lab 7) |
| `lab-09` | + agente revisor de seguridad (Lab 8) |
| `final` | + workflow, integración continua y hoja de ruta (Lab 9) |
