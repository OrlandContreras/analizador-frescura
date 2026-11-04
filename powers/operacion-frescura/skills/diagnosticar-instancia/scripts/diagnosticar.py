"""Diagnostica una instancia del Analizador de frescura sin enviar fotos al modelo.

Uso:
    python diagnosticar.py --participante oc [--minutos 30]
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import time
import urllib.error
import urllib.request


def pedir(url: str, metodo: str = "GET", cuerpo: dict | None = None) -> tuple[int, str]:
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(url, data=datos, method=metodo, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, str(e)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--participante", required=True)
    p.add_argument("--minutos", type=int, default=30)
    p.add_argument("--region", default="us-east-1")
    args = p.parse_args(argv)

    import boto3
    from botocore.exceptions import ClientError

    resultados: list[tuple[str, str, str]] = []
    pila_nombre = f"Frescura-{args.participante}"

    # 1. Stack y salidas
    try:
        pila = boto3.client("cloudformation", region_name=args.region).describe_stacks(StackName=pila_nombre)
        pila = pila["Stacks"][0]
        salidas = {s["OutputKey"]: s["OutputValue"] for s in pila.get("Outputs", [])}
        faltan = {"UrlApi", "GrupoRegistros"} - salidas.keys()
        estado = "OK" if not faltan else "FALLA"
        detalle = f"{pila['StackStatus']}; faltan: {', '.join(faltan) or 'ninguna'}"
        resultados.append(("Stack y salidas", estado, detalle))
    except ClientError as e:
        resultados.append(("Stack y salidas", "FALLA", f"No existe {pila_nombre}: {e.response['Error']['Code']}"))
        imprimir(resultados)
        sys.exit(1)
    url_api = salidas.get("UrlApi", "").rstrip("/")

    # 2. Salud
    codigo, texto = pedir(f"{url_api}/salud")
    ok = codigo == 200 and '"ok"' in texto
    resultados.append(("GET /salud", "OK" if ok else "FALLA", f"{codigo} {texto[:120]}"))

    # 3. Validación: contenido que no es imagen -> 415
    falsa = base64.b64encode(b"esto no es una imagen").decode()
    codigo, texto = pedir(f"{url_api}/analisis", "POST", {"imagen_base64": falsa, "tienda": "T-DIAGNOSTICO"})
    ok = codigo == 415 and "FORMATO_NO_SOPORTADO" in texto
    resultados.append(("Validación de imagen (espera 415)", "OK" if ok else "FALLA", f"{codigo} {texto[:120]}"))

    # 4. Registros recientes
    grupo = salidas.get("GrupoRegistros")
    if grupo:
        logs = boto3.client("logs", region_name=args.region)
        desde = int((time.time() - args.minutos * 60) * 1000)
        eventos, token = [], None
        while True:
            extra = {"nextToken": token} if token else {}
            r = logs.filter_log_events(logGroupName=grupo, startTime=desde, **extra)
            eventos += [e["message"] for e in r.get("events", [])]
            token = r.get("nextToken")
            if not token or len(eventos) > 5000:
                break
        analisis = sum(1 for m in eventos if '"evento": "analisis"' in m)
        fallos = [m for m in eventos if "Falló el análisis" in m or "Exception" in m]
        detalle = f"{analisis} análisis y {len(fallos)} fallos en {args.minutos} min"
        if fallos:
            ultimo = next((ln for ln in reversed(fallos[-1].splitlines()) if "Exception" in ln), fallos[-1])
            detalle += f". Último fallo: {ultimo.strip()[:160]}"
        resultados.append(("Registros recientes", "OK" if not fallos else "ATENCIÓN", detalle))

    imprimir(resultados)


def imprimir(resultados: list[tuple[str, str, str]]) -> None:
    print("| Comprobación | Resultado | Detalle |")
    print("| --- | --- | --- |")
    for nombre, estado, detalle in resultados:
        print(f"| {nombre} | {estado} | {detalle.replace('|', '/')} |")
    sano = all(e == "OK" for _, e, _ in resultados)
    print(f"\nVeredicto: {'Instancia sana' if sano else 'Requiere atención'}")


if __name__ == "__main__":
    main()
