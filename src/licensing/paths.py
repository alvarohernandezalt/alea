"""Platform-specific data paths for licensing artefacts."""

import os
import sys
from pathlib import Path

_APP_DIR_NAME = ".aleatoriccomposer"


def data_dir() -> Path:
    """Return (and create) the per-user hidden data directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    d = base / _APP_DIR_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def app_root() -> Path:
    """Return the directory where the running executable (or script) lives.

    For a PyInstaller bundle this is the folder containing the .exe.
    For a normal Python invocation it is the project root (parent of src/).
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    # Development: project root = src/../
    return Path(__file__).resolve().parent.parent.parent
