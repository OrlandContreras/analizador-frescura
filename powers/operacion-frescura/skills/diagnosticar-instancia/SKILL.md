---
name: diagnosticar-instancia
description: Diagnostica una instancia desplegada del Analizador de frescura - salud de la API, validación de imágenes y errores recientes en los registros de CloudWatch. Úsala cuando la web o la API fallen (por ejemplo, error 502) o cuando pidan revisar la salud de la instancia.
---

# Diagnóstico de una instancia del analizador

## Qué necesitas

- El identificador del participante con el que se desplegó la instancia (por ejemplo `oc`). Si no lo sabes, pregúntalo.
- El entorno de Python del proyecto (tiene `boto3`).

> **Qué Python usar:** el del entorno del proyecto, que tiene `boto3`. En Windows es `.venv\Scripts\python.exe`; en macOS o Linux, `.venv/bin/python`. Si no existe `.venv`, usa `python` (o `python3`) y avisa que hay que activar el entorno. En los comandos de abajo, `python` significa ese intérprete.

## Pasos

1. Ejecuta el script de esta skill, `scripts/diagnosticar.py`. En el proyecto `analizador-frescura` la ruta es `powers/operacion-frescura/skills/diagnosticar-instancia/scripts/diagnosticar.py`:

   ```
   python powers/operacion-frescura/skills/diagnosticar-instancia/scripts/diagnosticar.py --participante <id> --minutos 30
   ```

   El script hace cuatro comprobaciones, sin enviar fotos al modelo:
   1. Que el stack `Frescura-<id>` exista y tenga sus salidas.
   2. `GET /salud` responde `{"estado": "ok"}`.
   3. `POST /analisis` con un contenido que no es imagen responde `415 FORMATO_NO_SOPORTADO` (la validación funciona).
   4. Los registros de los últimos minutos: cuántos análisis hubo y si hubo fallos de visión.

2. Interpreta cada comprobación que no salga `OK` con `references/errores-comunes.md` y explica la causa probable y el siguiente paso.

3. Entrega una tabla con las cuatro comprobaciones (comprobación, resultado, qué hacer) y un veredicto de una línea: **Instancia sana** o **Requiere atención**.

## Reglas

- No despliegues, no borres ni cambies recursos. Si la solución requiere `cdk deploy`, dale el comando a la persona para que lo ejecute ella.
- No pidas ni muestres credenciales.
