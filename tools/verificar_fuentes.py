"""Verifica la coherencia del manifiesto de procedencia del snapshot orbital.

Comprueba los seis grupos, el total declarado, el formato del SHA-256 por grupo,
la URL de origen y las fechas. No descarga nada ni valida los TLE contra
CelesTrak: valida la coherencia interna del manifiesto.

    python tools/verificar_fuentes.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MANIFIESTO = RAIZ / "app" / "content" / "orbita.sources.json"
GRUPOS_ESPERADOS = 6
REGISTROS_ESPERADOS = 12308
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def main() -> int:
    if not MANIFIESTO.exists():
        print(f"ERROR: no existe el manifiesto: {MANIFIESTO}")
        return 1
    datos = json.loads(MANIFIESTO.read_text(encoding="utf-8"))
    for campo in ("downloaded_at", "groups", "reference_epoch", "epoch_min", "epoch_max"):
        if campo not in datos:
            print(f"ERROR: falta «{campo}» en el manifiesto")
            return 1
    grupos = datos["groups"]
    if len(grupos) != GRUPOS_ESPERADOS:
        print(f"ERROR: se esperaban {GRUPOS_ESPERADOS} grupos, hay {len(grupos)}")
        return 1
    total = 0
    for grupo in grupos:
        nombre = grupo.get("label") or grupo.get("id") or "?"
        cantidad = grupo.get("count")
        if not isinstance(cantidad, int) or cantidad <= 0:
            print(f"ERROR: grupo {nombre} con recuento inválido")
            return 1
        total += cantidad
        if not SHA256.match(str(grupo.get("sha256", ""))):
            print(f"ERROR: grupo {nombre} sin SHA-256 válido")
            return 1
        if not str(grupo.get("source", "")).startswith("https://"):
            print(f"ERROR: grupo {nombre} sin URL de origen")
            return 1
    if total != REGISTROS_ESPERADOS:
        print(f"ERROR: total {total}, esperado {REGISTROS_ESPERADOS}")
        return 1
    try:
        datetime.fromisoformat(str(datos["downloaded_at"]).replace("Z", "+00:00"))
        datetime.fromisoformat(str(datos["reference_epoch"]).replace("Z", "+00:00"))
    except ValueError as exc:
        print(f"ERROR: fecha no interpretable: {exc}")
        return 1
    print(f"OK: {len(grupos)} grupos - {total} registros - descarga {datos['downloaded_at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


