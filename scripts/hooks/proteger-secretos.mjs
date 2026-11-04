#!/usr/bin/env node
// Hook PreToolUse (Lab 6): bloquea cualquier herramienta que intente usar el archivo .env.
// En PreToolUse, una salida distinta de cero bloquea la herramienta y el mensaje de stderr llega al agente.
// Se permite .env.example, que no contiene secretos.

let entrada = '';
for await (const parte of process.stdin) entrada += parte;

const tocaEnv = /(^|[\s"'`/\\=])\.env(?![\w.-])/.test(entrada);

if (tocaEnv) {
  process.stderr.write(
    'Bloqueado por el hook proteger-secretos: el archivo .env contiene secretos y el agente no puede usarlo. ' +
      'Usa .env.example para conocer las variables necesarias.\n',
  );
  process.exit(2);
}

process.exit(0);
