"""Lane B — Activation-code validation at startup."""

from typing import Tuple

from src.licensing import clock_guard, code_core, code_store


def check_activation() -> Tuple[bool, str]:
    """Check stored activation code.

    Returns (ok, message).
    If not ok and no stored code exists, the caller should show
    the unlock dialog.
    """
    code = code_store.load()
    if code is None:
        return False, "NO_CODE"

    expiry = code_core.decode(code)
    if expiry is None:
        code_store.clear()
        return False, "El código guardado no es válido."

    if not clock_guard.check():
        return (
            False,
            "El reloj del sistema parece haber sido retrasado.\n"
            "Restaura la fecha correcta e inténtalo de nuevo.",
        )

    if code_core.is_expired(code):
        code_store.clear()
        return (
            False,
            f"Tu código expiró el {expiry.strftime('%d/%m/%Y')}.\n"
            "Introduce un nuevo código para continuar.",
        )

    clock_guard.stamp()
    return True, "OK"


def try_activate(code: str) -> Tuple[bool, str]:
    """Validate and store a new activation code.

    Returns (ok, message).
    """
    expiry = code_core.decode(code)
    if expiry is None:
        return False, "Código inválido. Verifica e inténtalo de nuevo."

    if code_core.is_expired(code):
        return False, f"Este código ya expiró el {expiry.strftime('%d/%m/%Y')}."

    if not clock_guard.check():
        return False, "El reloj del sistema parece haber sido retrasado."

    code_store.save(code)
    clock_guard.stamp()
    return True, f"Activado hasta el {expiry.strftime('%d/%m/%Y')}."
