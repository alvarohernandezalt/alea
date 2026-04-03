"""Lane B — Persist the activation code to a hidden file."""

from pathlib import Path
from typing import Optional

from src.licensing.paths import data_dir

_FILENAME = ".activation"


def _file() -> Path:
    return data_dir() / _FILENAME


def load() -> Optional[str]:
    """Return the stored activation code, or None."""
    f = _file()
    if not f.exists():
        return None
    try:
        code = f.read_text().strip()
        return code if code else None
    except OSError:
        return None


def save(code: str) -> None:
    """Persist an activation code."""
    _file().write_text(code)


def clear() -> None:
    """Remove the stored activation code."""
    f = _file()
    if f.exists():
        try:
            f.unlink()
        except OSError:
            pass
