"""Analiza una foto desde tu computador con Amazon Bedrock, sin desplegar nada.

Uso (desde la raíz del proyecto, con credenciales de AWS configuradas):

    python scripts/analizar_foto.py ruta/a/la/foto.jpg [--gramos 150]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from frescura.analizador import analizar_foto  # noqa: E402
from frescura.handler import detectar_formato  # noqa: E402
from frescura.vision import VisionBedrock  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("foto", type=Path)
    parser.add_argument("--gramos", type=float, default=100)
    args = parser.parse_args()

    imagen = args.foto.read_bytes()
    formato = detectar_formato(imagen)
    if formato is None:
        print("La foto debe ser JPEG o PNG.", file=sys.stderr)
        return 1
    resultado = analizar_foto(VisionBedrock(), imagen, formato, args.gramos)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
