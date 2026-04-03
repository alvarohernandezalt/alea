import sys

from PySide6.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def _check_license(app: QApplication) -> bool:
    """Run license validation (Lane A then Lane B fallback).

    Returns True if the app is allowed to launch.
    """
    from src.licensing import license_check, code_check
    from src.gui.dialogs.license_dialog import LicenseDialog
    from src.gui.dialogs.unlock_dialog import UnlockDialog

    # --- Lane A: try license.json first ---
    ok, msg, _lic = license_check.validate()
    if ok:
        return True

    # If license file exists but is expired/invalid, show message
    if msg != "No se encontró el archivo de licencia.":
        dlg = LicenseDialog("Licencia", msg)
        dlg.exec()
        return False

    # --- Lane B: no license file → ask for unlock code ---
    ok_code, msg_code = code_check.check_activation()
    if ok_code:
        return True

    # Show unlock dialog
    prompt_msg = "" if msg_code == "NO_CODE" else msg_code
    dlg = UnlockDialog(message=prompt_msg)

    from src.licensing.code_check import try_activate
    dlg.set_validator(try_activate)

    result = dlg.exec()
    return result == UnlockDialog.Accepted


def main():
    app = QApplication(sys.argv)

    if not _check_license(app):
        sys.exit(0)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
