---
name: resumen-uso
description: Resume el uso del Analizador de frescura por canal (personal y clientes), por tienda y por producto a partir del historial guardado en DynamoDB. Úsala cuando pregunten cuánto se ha usado el analizador, cómo va el uso por tienda o qué productos se analizan más.
---

# Resumen de uso del analizador

## Qué necesitas

- El identificador del participante con el que se desplegó la instancia (el valor de `-c participante=...`, por ejemplo `oc`). Si no lo sabes, pregúntalo antes de seguir.
- El entorno de Python del proyecto (tiene `boto3`).

> **Qué Python usar:** el del entorno del proyecto, que tiene `boto3`. En Windows es `.venv\Scripts\python.exe`; en macOS o Linux, `.venv/bin/python`. Si no existe `.venv`, usa `python` (o `python3`) y avisa que hay que activar el entorno. En los comandos de abajo, `python` significa ese intérprete.

## Pasos

1. Ejecuta el script de esta skill, `scripts/resumen_uso.py`. En el proyecto `analizador-frescura` la ruta es `powers/operacion-frescura/skills/resumen-uso/scripts/resumen_uso.py`:

   ```
   python powers/operacion-frescura/skills/resumen-uso/scripts/resumen_uso.py --participante <id> --salida docs/uso-piloto.md
   ```

   El script busca la tabla en las salidas del stack `Frescura-<id>`, lee el historial (solo lectura) y escribe el resumen en Markdown.

2. Si el script dice que el stack no existe o que la tabla está vacía, ofrece usar los datos de ejemplo de esta skill y avisa que **no son datos reales**:

   ```
   python powers/operacion-frescura/skills/resumen-uso/scripts/resumen_uso.py --archivo powers/operacion-frescura/skills/resumen-uso/references/historial-ejemplo.json --salida docs/uso-piloto.md
   ```

3. Lee `docs/uso-piloto.md` y responde con:
   - el total de análisis, cuántos son del personal y cuántos de clientes, y el número de tiendas;
   - la tienda con más uso y el producto más analizado;
   - el porcentaje de análisis **del personal** con confianza menor a 0,70, que según la política POL-FRV-001 van a **revisión humana**. Si pasa del 20%, recomiéndalo como el primer punto a mejorar del piloto.

## Reglas

- No modifiques ni borres registros de DynamoDB. Este análisis es de solo lectura.
- No inventes cifras: usa solo lo que imprime el script.
- El historial no guarda fotos ni datos de clientes. Si alguien pide datos personales, explica que no existen en el historial.
