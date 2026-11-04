#!/usr/bin/env node
// Hook PreToolUse (Lab 6): el agente no puede desplegar ni borrar la infraestructura.
// Desplegar crea recursos con costo en AWS: lo decide y lo ejecuta una persona en la terminal.

let entrada = '';
for await (const parte of process.stdin) entrada += parte;

const despliega = /\bcdk\s+(deploy|destroy)\b/i.test(entrada);

if (despliega) {
  process.stderr.write(
    'Bloqueado por el hook bloquear-despliegue: el agente no ejecuta cdk deploy ni cdk destroy. ' +
      'Indica a la persona el comando exacto para que lo ejecute ella en la terminal.\n',
  );
  process.exit(2);
}

process.exit(0);
