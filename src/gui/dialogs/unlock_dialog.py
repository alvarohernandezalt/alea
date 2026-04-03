"""Lane B — Dialog for entering an unlock code."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class UnlockDialog(QDialog):
    """Modal dialog where the student enters an activation code.

    Emits ``code_accepted(str)`` with the validated code on success.
    If the user cancels, the dialog is rejected (result == QDialog.Rejected).
    """

    code_accepted = Signal(str)

    def __init__(self, message: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Activar Aleatoric Composer")
        self.setFixedSize(500, 280)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(28, 24, 28, 24)

        # Header
        header = QLabel("Activar Aleatoric Composer")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #FBAD17;"
        )
        layout.addWidget(header)

        # Optional message (e.g. "código expirado")
        if message:
            msg = QLabel(message)
            msg.setWordWrap(True)
            msg.setAlignment(Qt.AlignCenter)
            msg.setStyleSheet("font-size: 13px; color: #E5E1DE;")
            layout.addWidget(msg)

        # Instruction
        instr = QLabel("Introduce el código que te proporcionó tu profesor:")
        instr.setStyleSheet("font-size: 12px; color: #B9AFA9;")
        layout.addWidget(instr)

        # Code input
        self._input = QLineEdit()
        self._input.setPlaceholderText("SUR-XXXX-XXXX-XXXXX")
        self._input.setMaxLength(20)
        self._input.setAlignment(Qt.AlignCenter)
        self._input.setStyleSheet(
            "QLineEdit { background-color: #303C42; color: #E5E1DE; "
            "border: 1px solid #3D4A51; border-radius: 4px; padding: 10px; "
            "font-size: 16px; font-family: 'Consolas', 'DM Mono', monospace; "
            "letter-spacing: 2px; }"
            "QLineEdit:focus { border-color: #FBAD17; }"
        )
        layout.addWidget(self._input)

        # Feedback label
        self._feedback = QLabel("")
        self._feedback.setAlignment(Qt.AlignCenter)
        self._feedback.setStyleSheet("font-size: 11px; color: #FF8C00;")
        layout.addWidget(self._feedback)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self._btn_activate = QPushButton("Activar")
        self._btn_activate.setStyleSheet(
            "QPushButton { background-color: #005A65; color: #E5E1DE; "
            "border: none; border-radius: 4px; padding: 8px 20px; "
            "font-weight: bold; }"
            "QPushButton:hover { background-color: #00897B; }"
        )
        self._btn_activate.clicked.connect(self._on_activate)

        btn_cancel = QPushButton("Cerrar")
        btn_cancel.setStyleSheet(
            "QPushButton { background-color: #303C42; color: #E5E1DE; "
            "border: 1px solid #3D4A51; border-radius: 4px; padding: 8px 20px; }"
            "QPushButton:hover { border-color: #FBAD17; }"
        )
        btn_cancel.clicked.connect(self.reject)

        btn_row.addStretch()
        btn_row.addWidget(self._btn_activate)
        btn_row.addWidget(btn_cancel)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Dialog background
        self.setStyleSheet("QDialog { background-color: #1E282D; }")

        # Validation callback — set by the caller
        self._validator = None

    def set_validator(self, fn):
        """Set a callable(code_str) -> (bool, message) for live validation."""
        self._validator = fn

    def _on_activate(self):
        code = self._input.text().strip()
        if not code:
            self._feedback.setText("Introduce un código.")
            return

        if self._validator:
            ok, msg = self._validator(code)
            if ok:
                self.code_accepted.emit(code)
                self.accept()
            else:
                self._feedback.setText(msg)
        else:
            self.code_accepted.emit(code)
            self.accept()
