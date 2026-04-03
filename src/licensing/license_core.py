"""Lane A — HMAC-signed license.json model and helpers."""

import hmac
import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from src.licensing._keys import get_key

_SIGN_FIELDS = ("workshop", "start_date", "expiry_date", "issued_at")


@dataclass
class License:
    workshop: str
    start_date: str  # YYYY-MM-DD
    expiry_date: str  # YYYY-MM-DD
    issued_at: str  # ISO 8601
    signature: str = ""

    # --- serialisation -------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "workshop": self.workshop,
            "start_date": self.start_date,
            "expiry_date": self.expiry_date,
            "issued_at": self.issued_at,
            "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "License":
        return cls(
            workshop=d["workshop"],
            start_date=d["start_date"],
            expiry_date=d["expiry_date"],
            issued_at=d["issued_at"],
            signature=d.get("signature", ""),
        )

    @classmethod
    def from_file(cls, path) -> "License":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def save(self, path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    # --- crypto --------------------------------------------------------------

    def _message(self) -> bytes:
        parts = "|".join(getattr(self, f) for f in _SIGN_FIELDS)
        return parts.encode("utf-8")

    def sign(self) -> None:
        self.signature = hmac.new(get_key(), self._message(), hashlib.sha256).hexdigest()

    def verify(self) -> bool:
        expected = hmac.new(get_key(), self._message(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.signature, expected)

    # --- date helpers --------------------------------------------------------

    def expiry(self) -> date:
        return date.fromisoformat(self.expiry_date)

    def is_expired(self) -> bool:
        return date.today() > self.expiry()

    def days_left(self) -> int:
        return (self.expiry() - date.today()).days


def create_license(
    workshop: str,
    start: date,
    expiry: date,
) -> License:
    """Create and sign a new license."""
    lic = License(
        workshop=workshop,
        start_date=start.isoformat(),
        expiry_date=expiry.isoformat(),
        issued_at=datetime.now().isoformat(timespec="seconds"),
    )
    lic.sign()
    return lic
