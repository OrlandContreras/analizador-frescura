"""Mide el acierto del analizador sobre fotos etiquetadas.

Uso (desde la raíz del proyecto):

    python eval/evaluar.py                 # modo ejemplo: lecturas fijas, sin costo ni fotos
    python eval/evaluar.py --modo bedrock  # modo real: analiza las fotos de eval/fotos con Bedrock

Escribe el resultado en eval/reporte.md y termina con código 1 si el acierto de etapa
queda por debajo del mínimo (--minimo, 85 por defecto).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "app"))

from frescura.catalogo import obtener_producto  # noqa: E402
from frescura.reglas import ETAPAS, etapa_madurez  # noqa: E402
from frescura.vision import normalizar_lectura  # noqa: E402

CARPETA = RAIZ / "eval"
UMBRAL_CONFIANZA = 0.70


def leer_etiquetas() -> list[dict]:
    with open(CARPETA / "etiquetas.csv", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def lecturas_ejemplo() -> dict:
    return json.loads((CARPETA / "lecturas_ejemplo.json").read_text(encoding="utf-8"))["lecturas"]


def lectura_bedrock(vision, archivo: str):
    ruta = CARPETA / "fotos" / archivo
    formato = "png" if ruta.suffix.lower() == ".png" else "jpeg"
    return vision.analizar(ruta.read_bytes(), formato)


def evaluar(modo: str) -> dict:
    etiquetas = leer_etiquetas()
    if modo == "bedrock":
        from frescura.vision import VisionBedrock

        vision = VisionBedrock()
    else:
        ejemplos = lecturas_ejemplo()

    filas = []
    for fila in etiquetas:
        if modo == "bedrock":
            lectura = lectura_bedrock(vision, fila["archivo"])
        else:
            lectura = normalizar_lectura(ejemplos[fila["archivo"]])
        producto = obtener_producto(lectura.producto)
        etapa = etapa_madurez(lectura.indice_madurez, producto["umbrales"]) if producto else None
        filas.append(
            {
                **fila,
                "producto_leido": lectura.producto,
                "etapa_leida": etapa,
                "confianza": lectura.confianza,
                "revisar": lectura.confianza < UMBRAL_CONFIANZA,
            }
        )

    total = len(filas)
    acierto_producto = sum(f["producto"] == f["producto_leido"] for f in filas) / total
    acierto_etapa = sum(f["producto"] == f["producto_leido"] and f["etapa"] == f["etapa_leida"] for f in filas) / total
    por_etapa = {}
    for etapa in ETAPAS:
        del_grupo = [f for f in filas if f["etapa"] == etapa]
        aciertos = sum(f["producto"] == f["producto_leido"] and f["etapa_leida"] == etapa for f in del_grupo)
        por_etapa[etapa] = (aciertos, len(del_grupo))
    confusiones = Counter(
        (f["etapa"], f["etapa_leida"] or "sin etapa") for f in filas if f["etapa"] != f["etapa_leida"]
    )
    return {
        "modo": modo,
        "total": total,
        "acierto_producto": acierto_producto,
        "acierto_etapa": acierto_etapa,
        "por_etapa": por_etapa,
        "confusiones": confusiones,
        "revisar": sum(f["revisar"] for f in filas),
        "errores": [f for f in filas if f["producto"] != f["producto_leido"] or f["etapa"] != f["etapa_leida"]],
    }


def escribir_reporte(r: dict, minimo: float) -> str:
    estado = "CUMPLE" if r["acierto_etapa"] * 100 >= minimo else "NO CUMPLE"
    lineas = [
        "# Reporte de evaluación del analizador",
        "",
        f"- Modo: **{r['modo']}**",
        f"- Fotos evaluadas: **{r['total']}**",
        f"- Acierto de producto: **{r['acierto_producto']:.1%}**",
        f"- Acierto de etapa: **{r['acierto_etapa']:.1%}** (mínimo {minimo:.0f}%: **{estado}**)",
        f"- Casos con confianza menor a {UMBRAL_CONFIANZA:.2f} (irían a revisión humana): **{r['revisar']}**",
        "",
        "## Acierto por etapa",
        "",
        "| Etapa real | Aciertos | Fotos | Acierto |",
        "| --- | --- | --- | --- |",
    ]
    for etapa, (aciertos, total) in r["por_etapa"].items():
        lineas.append(f"| {etapa} | {aciertos} | {total} | {aciertos / total:.0%} |")
    lineas += ["", "## Confusiones de etapa", "", "| Etapa real | Etapa leída | Casos |", "| --- | --- | --- |"]
    for (real, leida), casos in r["confusiones"].most_common():
        lineas.append(f"| {real} | {leida} | {casos} |")
    lineas += ["", "## Fotos con error", "", "| Archivo | Real | Leído |", "| --- | --- | --- |"]
    for f in r["errores"]:
        lineas.append(
            f"| {f['archivo']} | {f['producto']} / {f['etapa']} | {f['producto_leido']} / {f['etapa_leida'] or '-'} |"
        )
    texto = "\n".join(lineas) + "\n"
    (CARPETA / "reporte.md").write_text(texto, encoding="utf-8")
    return texto


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--modo", choices=["ejemplo", "bedrock"], default="ejemplo")
    parser.add_argument("--minimo", type=float, default=85.0, help="Acierto mínimo de etapa, en porcentaje")
    args = parser.parse_args()
    resultado = evaluar(args.modo)
    escribir_reporte(resultado, args.minimo)
    print(f"Acierto de producto: {resultado['acierto_producto']:.1%}")
    print(f"Acierto de etapa:    {resultado['acierto_etapa']:.1%} (mínimo {args.minimo:.0f}%)")
    print(f"Reporte: {CARPETA / 'reporte.md'}")
    return 0 if resultado["acierto_etapa"] * 100 >= args.minimo else 1


if __name__ == "__main__":
    sys.exit(main())
