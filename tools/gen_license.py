#!/usr/bin/env python3
"""Generate a signed license.json for Aleatoric Composer workshops.

Usage:
    python tools/gen_license.py \
        --workshop "Taller Composición Aleatoria 2026" \
        --start 2026-04-01 \
        --expiry 2026-04-30 \
        --output license.json
"""

import argparse
import sys
from datetime import date
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.licensing.license_core import create_license


def main():
    parser = argparse.ArgumentParser(
        description="Genera un fichero license.json firmado con HMAC."
    )
    parser.add_argument(
        "--workshop", required=True, help="Nombre del taller"
    )
    parser.add_argument(
        "--start",
        required=False,
        default=date.today().isoformat(),
        help="Fecha de inicio (YYYY-MM-DD). Default: hoy",
    )
    parser.add_argument(
        "--expiry", required=True, help="Fecha de expiración (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--output",
        default="license.json",
        help="Ruta del fichero de salida (default: license.json)",
    )
    args = parser.parse_args()

    start = date.fromisoformat(args.start)
    expiry = date.fromisoformat(args.expiry)

    if expiry <= start:
        print("ERROR: La fecha de expiración debe ser posterior a la de inicio.", file=sys.stderr)
        sys.exit(1)

    lic = create_license(args.workshop, start, expiry)
    lic.save(args.output)

    print(f"Licencia generada: {args.output}")
    print(f"  Taller:     {lic.workshop}")
    print(f"  Inicio:     {lic.start_date}")
    print(f"  Expiración: {lic.expiry_date}")
    print(f"  Firma:      {lic.signature[:16]}...")


if __name__ == "__main__":
    main()
