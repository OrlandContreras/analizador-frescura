# Errores comunes del Analizador de frescura

| Síntoma | Causa probable | Qué hacer |
| --- | --- | --- |
| El stack `Frescura-<id>` no existe | No se desplegó o se borró con `cdk destroy` | Desplegar con `cd infra` y `cdk deploy -c participante=<id>` (lo ejecuta la persona) |
| `/salud` no responde o da error de conexión | La URL está mal copiada o el stack quedó a medio desplegar | Revisar la salida `UrlApi` del stack y el estado en CloudFormation |
| `/salud` responde 429 `Too Many Requests` | Se superó el límite del taller (5 por segundo, ráfaga de 10) | Esperar unos segundos |
| La prueba de validación no responde 415 | El código desplegado no es el del repositorio | Correr `pytest` y volver a desplegar |
| Registros con "Falló el análisis de la imagen" y `AccessDeniedException` | El modelo de Bedrock no está habilitado en la cuenta o la política no incluye el perfil de inferencia | Habilitar Amazon Nova 2 Lite en Bedrock (equipo de AWS) y revisar la política en `infra/stacks/frescura_stack.py` |
| Registros con `ThrottlingException` | Bedrock limitó las llamadas | Reintentar; para el piloto, pedir aumento de cuota |
| Registros con `ValidationException` | La imagen no es válida para el modelo o el identificador del modelo cambió | Revisar `MODELO_VISION` y probar con otra foto |
| Ningún análisis en los registros | Nadie ha usado la instancia en ese periodo | Probar desde el celular con `UrlWeb` |
