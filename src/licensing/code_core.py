"""Lane B — Encode/decode unlock codes with embedded expiry date.

Code format:  SUR-XXXX-XXXX-XXXX  (16 chars, grouped in 4)

Internal layout (8 raw bytes before encoding):
  bytes 0-1 : expiry date as days since 2025-01-01  (uint16 BE)
  bytes 2-7 : truncated HMAC-SHA256 of bytes 0-1    (6 bytes)

The 8 bytes are encoded with a custom base32 alphabet that excludes
visually ambiguous characters (0, O, 1, I, L).
"""

import hmac
import hashlib
import struct
from datetime import date

from src.licensing._keys import get_key

_EPOCH = date(2025, 1, 1)
_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"  # 30 chars
_PREFIX = "SUR"


def _days_from_epoch(d: date) -> int:
    return (d - _EPOCH).days


def _date_from_days(n: int) -> date:
    from datetime import timedelta
    return _EPOCH + timedelta(days=n)


def _hmac_truncated(payload: bytes, length: int = 6) -> bytes:
    return hmac.new(get_key(), payload, hashlib.sha256).digest()[:length]


def _encode_bytes(data: bytes) -> str:
    """Encode 8 bytes into 13 base-30 characters."""
    n = int.from_bytes(data, "big")
    chars = []
    for _ in range(13):
        n, r = divmod(n, len(_ALPHABET))
        chars.append(_ALPHABET[r])
    return "".join(reversed(chars))


def _decode_bytes(s: str) -> bytes:
    """Decode 13 base-30 characters back to 8 bytes."""
    n = 0
    for c in s:
        n = n * len(_ALPHABET) + _ALPHABET.index(c.upper())
    return n.to_bytes(8, "big")


def _format_code(raw13: str) -> str:
    """Format as SUR-XXXX-XXXX-XXXXX."""
    # 13 chars → groups of 4-4-5
    return f"{_PREFIX}-{raw13[:4]}-{raw13[4:8]}-{raw13[8:]}"


def _strip_code(code: str) -> str:
    """Remove prefix and dashes, return uppercase 13-char body."""
    code = code.upper().replace("-", "").replace(" ", "")
    if code.startswith(_PREFIX):
        code = code[len(_PREFIX):]
    return code


# --- Public API --------------------------------------------------------------

def generate(expiry: date) -> str:
    """Generate an unlock code valid until *expiry*."""
    days = _days_from_epoch(expiry)
    payload = struct.pack(">H", days)
    mac = _hmac_truncated(payload)
    raw = _encode_bytes(payload + mac)
    return _format_code(raw)


def decode(code: str) -> date | None:
    """Decode and verify an unlock code.

    Returns the expiry date if valid, or None if the code is invalid.
    """
    body = _strip_code(code)
    if len(body) != 13:
        return None
    try:
        raw = _decode_bytes(body)
    except (ValueError, IndexError):
        return None
    payload = raw[:2]
    mac = raw[2:]
    expected = _hmac_truncated(payload)
    if not hmac.compare_digest(mac, expected):
        return None
    days = struct.unpack(">H", payload)[0]
    try:
        return _date_from_days(days)
    except (OverflowError, ValueError):
        return None


def is_expired(code: str) -> bool | None:
    """Check if a code is expired.  Returns None if code is invalid."""
    expiry = decode(code)
    if expiry is None:
        return None
    return date.today() > expiry
