---
inclusion: fileMatch
fileMatchPattern: ["infra/**/*.py"]
---
# Estándares de infraestructura en AWS

- **Mínimos privilegios:** cada permiso nombra el recurso exacto. Nunca `"*"` en acciones ni en recursos, salvo la región del modelo base de Bedrock, que lo exige el perfil de inferencia entre regiones.
- **Etiquetas:** todo recurso hereda `Proyecto`, `Participante` y `Entorno` desde `infra/app.py`. No las quites.
- **Nombres:** cada participante tiene su propio stack `Frescura-<participante>`. No pongas nombres fijos a recursos: deja que CDK los genere para que no choquen entre participantes.
- **Datos:** buckets privados, cifrados y con SSL obligatorio. Nada público salvo lo que sirve CloudFront.
- **Taller:** `RemovalPolicy.DESTROY` para que `cdk destroy` no deje recursos con costo.
- **Costo:** la API mantiene su límite de uso (10 de ráfaga, 5 por segundo) para proteger el costo de Bedrock.
- **Pruebas:** todo cambio de infraestructura se acompaña de una aserción en `tests/test_infra.py`.
- **Despliegue:** el agente nunca ejecuta `cdk deploy` ni `cdk destroy`. Lo hace una persona en la terminal.
