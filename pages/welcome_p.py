import os

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap

from pages.components.primary_button import PrimaryButton

from pages.constants import APP_FONT, BG, TEXT_D, TEXT_M, TEXT_L

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "images", "welc.png")


class WelcomePage(QWidget):
    go_signup = Signal()
    go_login = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background: {BG};")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 30, 32, 50)
        layout.setSpacing(0)

        # Icon area
        logo_label = QLabel()
        pixmap = QPixmap(img_path)
        scaled = pixmap.scaled(300, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("background: transparent;")
        layout.addWidget(logo_label)

        layout.addSpacing(24)

        # App name
        app_name = QLabel("HabitTracker")
        app_name.setFont(QFont(APP_FONT, 30, QFont.Bold))
        app_name.setAlignment(Qt.AlignCenter)
        app_name.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        layout.addWidget(app_name)

        layout.addSpacing(8)

        subtitle = QLabel("Build habits. Reach your goals.")
        subtitle.setFont(QFont(APP_FONT, 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addStretch()

        # Sign Up button
        btn_signup = PrimaryButton("Sign Up")
        btn_signup.clicked.connect(self.go_signup)
        layout.addWidget(btn_signup)

        layout.addSpacing(14)

        # Log In button
        btn_login = PrimaryButton("Log In")
        btn_login.clicked.connect(self.go_login)
        layout.addWidget(btn_login)

        layout.addSpacing(20)

        # Footer note
        footer = QLabel("Your data is stored locally on this device")
        footer.setFont(QFont(APP_FONT, 10))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet(f"color: {TEXT_L}; background: transparent;")
        footer.setWordWrap(True)
        layout.addWidget(footer)
