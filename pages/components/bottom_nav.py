from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.constants import *
from pages.utils.helpers import * 

class BottomNav(QWidget):
    NAV_H = 56

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(self.NAV_H)
        self.setStyleSheet(f"background: {WHITE};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        items = [("🏠", "Home", True), ("📈", "Activity", False), ("⚙️", "Settings", False)]
        for i, (ico, lbl, active) in enumerate(items):
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignCenter)
            ico_lbl = QLabel(ico)
            ico_lbl.setFont(QFont("Segoe UI Emoji", 20))
            ico_lbl.setAlignment(Qt.AlignCenter)
            ico_lbl.setStyleSheet(f"color: {ORANGE if active else TEXT_L}; background: transparent;")
            col.addWidget(ico_lbl)
            layout.addLayout(col)
