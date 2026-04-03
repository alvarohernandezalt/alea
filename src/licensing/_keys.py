"""Obfuscated secret key for HMAC signing.

The key is split across two XOR-masked constants to make casual
extraction from a decompiled binary non-trivial.  This is NOT
cryptographic security — it raises the bar just enough so that a
student would need reversing tools to forge a license/code.
"""

# Two halves, each 16 bytes, XOR-masked with a per-half pad.
# Real key = (_A ^ _PA) || (_B ^ _PB)
_A = b"\xc7\x3a\x91\x0f\x54\xe8\xb2\x6d\xa0\x19\x7c\xf3\x45\xde\x88\x2b"
_PA = b"\xa4\x59\xf2\x6c\x37\x8b\xd1\x0e\xc3\x7a\x1f\x90\x26\xbd\xeb\x48"

_B = b"\x1e\xd7\x63\xab\x80\x4c\xf5\x29\x76\xe1\x3d\xba\x08\x97\x5a\xc4"
_PB = b"\x7d\xb4\x00\xc8\xe3\x2f\x96\x4a\x15\x82\x5e\xd9\x6b\xf4\x39\xa7"


def _derive() -> bytes:
    """Recover the 32-byte HMAC key at runtime."""
    return bytes(a ^ p for a, p in zip(_A, _PA)) + bytes(
        b ^ p for b, p in zip(_B, _PB)
    )


def get_key() -> bytes:
    """Return the HMAC-SHA256 signing key."""
    return _derive()
