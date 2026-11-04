#!/usr/bin/env node
// Hook PostFileSave (Lab 6): corre ruff y pytest con el Python del entorno virtual del proyecto.
// Funciona en macOS, Linux y Windows.
import { existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

const candidatos = ['.venv/bin/python', '.venv/Scripts/python.exe'];
const python = candidatos.find((ruta) => existsSync(ruta));

if (!python) {
  console.error('No encontré el entorno virtual .venv. Créalo con las instrucciones de laboratorios/00-preparacion.');
  process.exit(1);
}

function correr(args) {
  const resultado = spawnSync(python, args, { encoding: 'utf8' });
  return { ok: resultado.status === 0, salida: `${resultado.stdout ?? ''}${resultado.stderr ?? ''}`.trim() };
}

const lint = correr(['-m', 'ruff', 'check', '.']);
const pruebas = correr(['-m', 'pytest', '-q']);
const resumen = pruebas.salida.split('\n').filter(Boolean).pop() ?? '';

if (lint.ok && pruebas.ok) {
  console.log(`Ruff sin problemas. Pruebas: ${resumen}`);
  process.exit(0);
}

if (!lint.ok) console.error(`Ruff encontró problemas:\n${lint.salida}`);
if (!pruebas.ok) console.error(`Las pruebas fallan:\n${pruebas.salida}`);
process.exit(1);
