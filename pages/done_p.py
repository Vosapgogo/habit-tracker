import os

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap

from .constants import APP_FONT, TEXT_D, TEXT_M, BG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "images", "done.png")

from pages.components.primary_button import PrimaryButton


class DonePage(QWidget):
    go_home = Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {BG};")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 30, 40, 60)
        layout.setSpacing(0)

        layout.addStretch()

        # Illustration
        logo_label = QLabel()
        pixmap = QPixmap(img_path)
        scaled = pixmap.scaled(300, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("background: transparent;")
        layout.addWidget(logo_label)

        layout.addSpacing(24)

        #  Title
        done_lbl = QLabel("Done!")
        done_lbl.setAlignment(Qt.AlignCenter)
        done_lbl.setFont(QFont(APP_FONT, 32, QFont.Bold))
        done_lbl.setStyleSheet(
            f"color: {TEXT_D}; background: transparent; border: none;"
        )
        layout.addWidget(done_lbl)
        layout.addSpacing(12)

        # Subtitle
        self.sub_lbl = QLabel("")
        self.sub_lbl.setAlignment(Qt.AlignCenter)
        self.sub_lbl.setWordWrap(True)
        self.sub_lbl.setFont(QFont(APP_FONT, 15))
        self.sub_lbl.setStyleSheet(
            f"color: {TEXT_M}; background: transparent; border: none;"
        )
        layout.addWidget(self.sub_lbl)
        layout.addSpacing(32)

        # Continue button
        cont_btn = PrimaryButton("Go to the home page")
        cont_btn.clicked.connect(self.go_home)
        layout.addWidget(cont_btn)

        layout.addStretch()

    def set_name(self, name):
        self.sub_lbl.setText(
            f"Congratulations, {name}!\nYour account has been created successfully"
        )
