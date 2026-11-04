# Laboratorios del workshop de Kiro

En este taller construyes y despliegas en AWS la primera versión del **Analizador de frescura de frutas y verduras**, trabajando con Kiro, el entorno de desarrollo con agentes de IA de AWS. Todos los participantes hacen todos los laboratorios, en orden.

> **¿Trabajas en el entorno que entrega AWS** (Kiro IDE en el navegador o en una máquina virtual)? Sigue [GUIA-ENTORNO-AWS.md](../GUIA-ENTORNO-AWS.md) en lugar de estas guías.

> **Antes del taller:** completa el [Lab 0 · Preparación del equipo](00-preparacion/README.md). Ahí están los prerrequisitos (Kiro IDE y CLI, Python, Node.js, pnpm, AWS CDK, AWS CLI, Git y uv), cómo instalarlos y cómo resolver los errores más comunes, incluidos los de pnpm.

## Laboratorios

| # | Laboratorio | Nivel | Tiempo | Rama de inicio |
| --- | --- | --- | --- | --- |
| 0 | [Preparación del equipo](00-preparacion/README.md) | — | Antes del taller | `lab-01` |
| 1 | [Primer contacto](01-primer-contacto/README.md) | L100 | 15 min | `lab-01` |
| 2 | [De la necesidad al plan](02-de-la-necesidad-al-plan/README.md) | L100 | 25 min | `lab-02` |
| 3 | [Construir con el plan](03-construir-con-el-plan/README.md) | L100 | 35 min | `lab-03` |
| 4 | [Calidad medible](04-calidad-medible/README.md) | L200 | 15 min | `lab-04` |
| — | Pausa | | 10 min | |
| 5 | [El "manual de la casa" y la memoria](05-manual-de-la-casa/README.md) | L200 | 20 min | `lab-05` |
| 6 | [Reglas automáticas](06-reglas-automaticas/README.md) | L200 | 15 min | `lab-06` |
| 7 | [Conectar y estandarizar](07-conectar-y-estandarizar/README.md) | L300 | 20 min | `lab-07` |
| 8 | [Agentes especializados y despliegue](08-agentes-y-despliegue/README.md) | L300 | 35 min | `lab-08` |
| 9 | [Operar con un Power](09-operar-con-un-power/README.md) | L300 | 15 min | `lab-09` |
| 10 | [Orquestar, entregar y cerrar](10-orquestar-entregar-y-cerrar/README.md) | L300 | 25 min | `lab-10` |

La rama `final` tiene el proyecto completo, como queda al terminar el Lab 10.

## Cómo funcionan las ramas

Cada rama `lab-NN` tiene el proyecto **tal como debe estar al empezar** ese laboratorio. Si terminas un laboratorio, sigues trabajando en tu propia copia. Si te atrasaste o algo se rompió, cambias a la rama del laboratorio siguiente y continúas con el grupo.

### Cambiar de rama (alcanzar al grupo)

En la terminal de Kiro, desde la carpeta del proyecto y con el entorno activo (los comandos son iguales en Windows y en macOS o Linux):

```bash
git stash --include-untracked
git switch lab-05
pip install -r requirements-dev.txt
```

- La primera línea guarda tus cambios a un lado (no se pierden).
- La segunda cambia a la rama del laboratorio. Cambia `lab-05` por la rama que necesites.
- La tercera instala las dependencias de esa rama, por si cambiaron.

Para ver en qué rama estás: `git branch --show-current`.

## Convenciones de las guías

- Los textos en un recuadro gris se **copian y pegan tal cual**, en el chat de Kiro o en la terminal, según diga el paso.
- **Windows y macOS o Linux:** cuando un comando cambia según el sistema, la guía muestra las dos versiones. En Windows, la terminal de Kiro es **PowerShell**. Cuando aparece un solo comando, es igual en los dos sistemas.
- Donde veas `<tus-iniciales>`, escribe tus iniciales en minúscula, sin espacios ni tildes (por ejemplo `oc`), **sin los signos `<` y `>`**. Así tu despliegue no choca con el de otra persona. En PowerShell, si dejas los signos aparece el error "The '<' operator is reserved for future use".
- Los nombres de botones y menús aparecen en **negrita**, como se ven en Kiro (en inglés).
- Las respuestas de Kiro cambian de una persona a otra. Lo importante es que cumplas el **Resultado esperado** de cada paso y el **Criterio de éxito** del laboratorio.
- **Regla de datos:** todos los datos de tienda del proyecto son ficticios. No pegues datos reales de clientes, precios ni inventario en Kiro.
