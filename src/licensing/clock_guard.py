"""Anti-clock-rollback guard.

On every successful launch we persist ``datetime.now()`` to a hidden
file.  On the next launch, if the system clock is *before* that
timestamp, the user has rolled back the clock and the check fails.
"""

from datetime import datetime
from pathlib import Path

from src.licensing.paths import data_dir

_FILENAME = ".last_seen"
_FMT = "%Y-%m-%dT%H:%M:%S"


def _file() -> Path:
    return data_dir() / _FILENAME


def check() -> bool:
    """Return True if the clock looks plausible (not rolled back)."""
    f = _file()
    if not f.exists():
        return True
    try:
        last = datetime.strptime(f.read_text().strip(), _FMT)
    except (ValueError, OSError):
        return True  # corrupted file — allow launch
    return datetime.now() >= last


def stamp() -> None:
    """Record the current time as last-seen."""
    try:
        _file().write_text(datetime.now().strftime(_FMT))
    except OSError:
        pass  # non-fatal — don't block the app
