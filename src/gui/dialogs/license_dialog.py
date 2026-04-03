"""Lane A — Dialog shown when the license is missing, invalid, or expired."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class LicenseDialog(QDialog):
    """Modal dialog that blocks app launch with a licensing message."""

    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(480, 220)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(28, 24, 28, 24)

        # Icon-like header
        header = QLabel(title)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #FBAD17;"
        )
        layout.addWidget(header)

        # Message body
        body = QLabel(message)
        body.setWordWrap(True)
        body.setAlignment(Qt.AlignCenter)
        body.setStyleSheet("font-size: 13px; color: #E5E1DE;")
        layout.addWidget(body)

        layout.addStretch()

        # Close button
        btn = QPushButton("Cerrar")
        btn.setFixedWidth(120)
        btn.setStyleSheet(
            "QPushButton { background-color: #303C42; color: #E5E1DE; "
            "border: 1px solid #3D4A51; border-radius: 4px; padding: 8px; }"
            "QPushButton:hover { border-color: #FBAD17; }"
        )
        btn.clicked.connect(self.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)

        # Dialog background
        self.setStyleSheet("QDialog { background-color: #1E282D; }")
