"""Lane A — License validation at startup."""

from pathlib import Path
from typing import Optional, Tuple

from src.licensing import clock_guard
from src.licensing.license_core import License
from src.licensing.paths import app_root, data_dir

_FILENAME = "license.json"


def _search_license() -> Optional[Path]:
    """Look for license.json in multiple locations (priority order)."""
    candidates = [
        app_root() / _FILENAME,          # next to .exe or project root
        data_dir() / _FILENAME,           # user data dir
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def validate() -> Tuple[bool, str, Optional[License]]:
    """Validate the license file.

    Returns (ok, message, license_or_None).
    """
    path = _search_license()
    if path is None:
        return False, "No se encontró el archivo de licencia.", None

    try:
        lic = License.from_file(path)
    except Exception:
        return False, "El archivo de licencia está corrupto.", None

    if not lic.verify():
        return False, "La firma de la licencia no es válida.", None

    if not clock_guard.check():
        return (
            False,
            "El reloj del sistema parece haber sido retrasado.\n"
            "Restaura la fecha correcta e inténtalo de nuevo.",
            lic,
        )

    if lic.is_expired():
        return (
            False,
            f"El taller «{lic.workshop}» finalizó el {lic.expiry_date}.\n"
            "Contacta con tu profesor para una nueva licencia.",
            lic,
        )

    # All good — stamp clock guard for next launch
    clock_guard.stamp()
    return True, "OK", lic
