#!/usr/bin/env python3
"""App de AWS CDK. Cada participante despliega su propia copia:

cdk deploy -c participante=<tus-iniciales>
"""

import re

import aws_cdk as cdk

from stacks.frescura_stack import FrescuraStack

app = cdk.App()

participante = (app.node.try_get_context("participante") or "").strip().lower()
if not re.fullmatch(r"[a-z][a-z0-9]{1,9}", participante):
    raise SystemExit(
        "Falta tu identificador. Usa: cdk deploy -c participante=<tus-iniciales> "
        "(de 2 a 10 letras o números, empezando con letra; por ejemplo oc o ocontreras)"
    )

modelo = app.node.try_get_context("modeloVision") or "us.amazon.nova-2-lite-v1:0"

FrescuraStack(
    app,
    f"Frescura-{participante}",
    participante=participante,
    modelo_vision=modelo,
    description=f"Analizador de frescura de frutas y verduras (workshop Kiro) - {participante}",
)

cdk.Tags.of(app).add("Proyecto", "analizador-frescura")
cdk.Tags.of(app).add("Participante", participante)
cdk.Tags.of(app).add("Entorno", "workshop")

app.synth()
