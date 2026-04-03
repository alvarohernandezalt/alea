#!/usr/bin/env python3
"""Generate an unlock code for Aleatoric Composer workshops.

Usage:
    python tools/gen_code.py --expiry 2026-04-30
    python tools/gen_code.py --expiry 2026-04-30 --batch 5
"""

import argparse
import sys
from datetime import date
from pathlib import Path

# Allow running from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.licensing.code_core import generate


def main():
    parser = argparse.ArgumentParser(
        description="Genera códigos de desbloqueo para Aleatoric Composer."
    )
    parser.add_argument(
        "--expiry", required=True, help="Fecha de expiración (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=1,
        help="Número de códigos a generar (default: 1). "
             "Todos comparten la misma fecha de expiración.",
    )
    args = parser.parse_args()

    expiry = date.fromisoformat(args.expiry)
    if expiry <= date.today():
        print("AVISO: La fecha de expiración ya ha pasado.", file=sys.stderr)

    print(f"Códigos válidos hasta: {expiry.isoformat()}\n")
    for i in range(args.batch):
        code = generate(expiry)
        print(f"  {code}")


if __name__ == "__main__":
    main()
