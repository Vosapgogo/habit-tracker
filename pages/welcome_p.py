from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient
from PySide6.QtGui import QPixmap

from pages.constants import WHITE, ORANGE, ORANGE_L, BG, TEXT_D, TEXT_M, TEXT_L, BORDER
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "images", "welc.png")

class WelcomePage(QWidget):
    """First screen: choose Sign Up or Log In"""

    go_signup = Signal()
    go_login  = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background: {BG};")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 60, 32, 50)
        layout.setSpacing(0)

        # ── Logo / Icon area ─────────────────────────────────────────────────
        logo_label = QLabel()
        pixmap = QPixmap(img_path)
        scaled = pixmap.scaled(300, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("background: transparent;")
        layout.addWidget(logo_label)

        layout.addSpacing(24)

        # ── App name ─────────────────────────────────────────────────────────
        app_name = QLabel("HabitTracker")
        app_name.setFont(QFont("Helvetica Neue", 30, QFont.Bold))
        app_name.setAlignment(Qt.AlignCenter)
        app_name.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        layout.addWidget(app_name)

        layout.addSpacing(8)

        subtitle = QLabel("Build habits. Reach your goals.")
        subtitle.setFont(QFont("Helvetica Neue", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
        layout.addWidget(subtitle)

        layout.addStretch()

        # ── Sign Up button ───────────────────────────────────────────────────
        btn_signup = QPushButton("Sign Up")
        btn_signup.setFixedHeight(52)
        btn_signup.setFont(QFont("Helvetica Neue", 15, QFont.Bold))
        btn_signup.setCursor(Qt.PointingHandCursor)
        btn_signup.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ORANGE}, stop:1 {ORANGE_L});
                color: {WHITE};
                border-radius: 26px;
                border: none;
            }}
            QPushButton:hover {{ background: {ORANGE_L}; }}
            QPushButton:pressed {{ background: #E05010; }}
        """)
        btn_signup.clicked.connect(self.go_signup)
        layout.addWidget(btn_signup)

        layout.addSpacing(14)

        # ── Log In button ────────────────────────────────────────────────────
        btn_login = QPushButton("Log In")
        btn_login.setFixedHeight(52)
        btn_login.setFont(QFont("Helvetica Neue", 15, QFont.Bold))
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setStyleSheet(f"""
            QPushButton {{
                background: {WHITE};
                color: {ORANGE};
                border-radius: 26px;
                border: 2px solid {ORANGE};
            }}
            QPushButton:hover {{ background: #FFF3EE; }}
            QPushButton:pressed {{ background: #FFE5D6; }}
        """)
        btn_login.clicked.connect(self.go_login)
        layout.addWidget(btn_login)

        layout.addSpacing(20)

        # ── Footer note ──────────────────────────────────────────────────────
        footer = QLabel("Your data is stored locally on this device")
        footer.setFont(QFont("Helvetica Neue", 10))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet(f"color: {TEXT_L}; background: transparent;")
        layout.addWidget(footer)