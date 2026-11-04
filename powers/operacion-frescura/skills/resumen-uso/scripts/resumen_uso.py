"""Resume el historial del Analizador de frescura por tienda y producto (solo lectura).

Uso:
    python resumen_uso.py --participante oc [--salida docs/uso-piloto.md]
    python resumen_uso.py --archivo historial-ejemplo.json [--salida docs/uso-piloto.md]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

UMBRAL_CONFIANZA = 0.70  # POL-FRV-001: por debajo va a revisión humana


def leer_dynamodb(participante: str, region: str) -> list[dict]:
    import boto3
    from botocore.exceptions import ClientError

    cfn = boto3.client("cloudformation", region_name=region)
    try:
        pila = cfn.describe_stacks(StackName=f"Frescura-{participante}")["Stacks"][0]
    except ClientError:
        sys.exit(f"No existe el stack Frescura-{participante} en {region}. Revisa el identificador o despliega.")
    salidas = {s["OutputKey"]: s["OutputValue"] for s in pila.get("Outputs", [])}
    tabla = boto3.resource("dynamodb", region_name=region).Table(salidas["TablaAnalisis"])
    registros, inicio = [], None
    while True:
        pagina = tabla.scan(**({"ExclusiveStartKey": inicio} if inicio else {}))
        registros += pagina.get("Items", [])
        inicio = pagina.get("LastEvaluatedKey")
        if not inicio:
            return registros


def resumir(registros: list[dict], origen: str) -> str:
    if not registros:
        return f"# Uso del analizador\n\nOrigen: {origen}\n\nEl historial está vacío: todavía no hay análisis.\n"
    por_tienda: dict[str, list[dict]] = defaultdict(list)
    for r in registros:
        por_tienda[r.get("tienda") or "sin-tienda"].append(r)
    productos = Counter(r.get("producto") or "desconocido" for r in registros)
    etapas = Counter(r.get("etapa") or "sin-etapa" for r in registros)
    bajas = sum(1 for r in registros if float(r.get("confianza", 0)) < UMBRAL_CONFIANZA)
    fechas = sorted(str(r["fecha"]) for r in registros if r.get("fecha"))

    lineas = [
        "# Uso del analizador",
        "",
        f"Origen: {origen}",
        "",
        f"- Análisis: **{len(registros)}** en **{len(por_tienda)}** tiendas",
    ]
    if fechas:
        lineas.append(f"- Periodo: {fechas[0][:16]} a {fechas[-1][:16]} (UTC)")
    lineas += [
        f"- Confianza menor a {UMBRAL_CONFIANZA:.2f} (revisión humana): **{bajas}** ({bajas / len(registros):.0%})",
        "",
        "## Por tienda",
        "",
        "| Tienda | Análisis | Producto más analizado | Confianza promedio | A revisión humana |",
        "| --- | --- | --- | --- | --- |",
    ]
    for tienda, filas in sorted(por_tienda.items(), key=lambda t: (-len(t[1]), t[0])):
        top = Counter(f.get("producto") or "desconocido" for f in filas).most_common(1)[0][0]
        prom = sum(float(f.get("confianza", 0)) for f in filas) / len(filas)
        rev = sum(1 for f in filas if float(f.get("confianza", 0)) < UMBRAL_CONFIANZA)
        lineas.append(f"| {tienda} | {len(filas)} | {top} | {prom:.2f} | {rev} |")
    lineas += ["", "## Por producto", "", "| Producto | Análisis |", "| --- | --- |"]
    lineas += [f"| {p} | {n} |" for p, n in productos.most_common()]
    lineas += ["", "## Por etapa", "", "| Etapa | Análisis |", "| --- | --- |"]
    lineas += [f"| {e} | {n} |" for e, n in etapas.most_common()]
    return "\n".join(lineas) + "\n"


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    fuente = p.add_mutually_exclusive_group(required=True)
    fuente.add_argument("--participante", help="Identificador usado en cdk deploy -c participante=...")
    fuente.add_argument("--archivo", help="JSON con registros de ejemplo")
    p.add_argument("--region", default="us-east-1")
    p.add_argument("--salida", help="Archivo Markdown donde guardar el resumen")
    args = p.parse_args(argv)

    if args.archivo:
        registros = json.loads(Path(args.archivo).read_text(encoding="utf-8"))
        origen = f"datos de ejemplo ({Path(args.archivo).name}), no son datos reales"
    else:
        registros = leer_dynamodb(args.participante, args.region)
        origen = f"tabla de DynamoDB del stack Frescura-{args.participante}"
    texto = resumir(registros, origen)
    if args.salida:
        Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
        Path(args.salida).write_text(texto, encoding="utf-8")
        print(f"Resumen guardado en {args.salida}\n")
    print(texto)


if __name__ == "__main__":
    main()
