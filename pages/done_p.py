from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont
from .constants import ORANGE, TEXT_D, TEXT_M, BG, ORANGE_L


class DonePage(QWidget):
    go_home = Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {BG};")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 60, 40, 60)
        layout.setSpacing(0)

        layout.addStretch()

        # ── Illustration - document + checkmark ──────────────────────
        icon_container = QLabel()
        icon_container.setAlignment(Qt.AlignCenter)
        icon_container.setFixedHeight(180)
        icon_container.setStyleSheet(f"""
            QLabel {{
                font-size: 100px;
                background: transparent;
                border: none;
            }}
        """)
        icon_container.setText("📋")
        layout.addWidget(icon_container, alignment=Qt.AlignCenter)

        # Green checkmark badge
        check_lbl = QLabel("✓")
        check_lbl.setAlignment(Qt.AlignCenter)
        check_lbl.setFixedSize(48, 48)
        check_lbl.setFont(QFont("", 22, QFont.Bold))
        check_lbl.setStyleSheet("""
            QLabel {
                background: #4CAF7D;
                color: white;
                border-radius: 24px;
                border: 3px solid white;
            }
        """)
        layout.addWidget(check_lbl, alignment=Qt.AlignCenter)
        layout.addSpacing(32)

        # ── "Done!" title ─────────────────────────────────────────────
        done_lbl = QLabel("Done!")
        done_lbl.setAlignment(Qt.AlignCenter)
        done_lbl.setFont(QFont("", 32, QFont.Bold))
        done_lbl.setStyleSheet(f"color: {TEXT_D}; background: transparent; border: none;")
        layout.addWidget(done_lbl)
        layout.addSpacing(12)

        # ── Subtitle ─────────────────────────────────────────────────
        self.sub_lbl = QLabel("Акаунт успішно створено!\nВітаємо на борту 🎉")
        self.sub_lbl.setAlignment(Qt.AlignCenter)
        self.sub_lbl.setWordWrap(True)
        self.sub_lbl.setFont(QFont("", 15))
        self.sub_lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent; border: none; line-height: 1.6;")
        layout.addWidget(self.sub_lbl)
        layout.addSpacing(48)

        # ── Continue button ───────────────────────────────────────────
        cont_btn = QPushButton("Перейти на головну →")
        cont_btn.setFixedHeight(56)
        cont_btn.setStyleSheet(ORANGE)
        cont_btn.setCursor(Qt.PointingHandCursor)
        cont_btn.clicked.connect(self.go_home)
        layout.addWidget(cont_btn)

        layout.addStretch()

    def set_name(self, name: str):
        self.sub_lbl.setText(f"Вітаємо, {name}!\nАкаунт успішно створено 🎉")
