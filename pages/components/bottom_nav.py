import os

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
from pages.constants import WHITE, BORDER

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


class BottomNav(QWidget):
    NAV_H = 56
    tab_requested = Signal(str)

    def __init__(self, active_tab="Home", parent=None):
        super().__init__(parent)
        self.active_tab = active_tab
        self.setFixedHeight(self.NAV_H)
        self.setStyleSheet(f"background: {WHITE}; border-top: 1px solid {BORDER};")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.items = [
            {"name": "Home", "icon": "home"},
            {"name": "Activity", "icon": "progress"},
            {"name": "Settings", "icon": "settings"},
        ]

        self._build_nav()

    def _build_nav(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for item in self.items:
            is_active = item["name"] == self.active_tab
            icon_filename = (
                f"on_{item['icon']}.png" if is_active else f"{item['icon']}.png"
            )
            icon_path = os.path.join(IMAGES_DIR, icon_filename)

            col = QWidget()
            col.setCursor(Qt.PointingHandCursor)
            col_layout = QVBoxLayout(col)
            col_layout.setContentsMargins(0, 8, 0, 8)
            col_layout.setAlignment(Qt.AlignCenter)

            ico_lbl = QLabel()
            ico_lbl.setStyleSheet("background: transparent; border: none;")
            pixmap = QPixmap(icon_path)

            if pixmap.isNull():
                print(f"ERROR: Failed to load image at: {icon_path}")

            ico_lbl.setPixmap(
                pixmap.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            ico_lbl.setAlignment(Qt.AlignCenter)
            col_layout.addWidget(ico_lbl)

            col.mousePressEvent = lambda e, name=item["name"]: self.tab_requested.emit(
                name
            )
            self.layout.addWidget(col)

    def set_active_tab(self, tab_name):
        self.active_tab = tab_name
        self._build_nav()
