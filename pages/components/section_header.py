from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.constants import *
from pages.utils.helpers import * 

class SectionHeader(QWidget):
    def __init__(self, title, link_text="See all", bg=WHITE, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(title)
        title_label.setFont(QFont("Helvetica Neue", 15, QFont.Bold))
        title_label.setStyleSheet(f"color: {TEXT_D}; background: transparent;")

        see_all = QLabel(link_text)
        see_all.setFont(QFont("Helvetica Neue", 11))
        see_all.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        see_all.setCursor(Qt.PointingHandCursor)

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(see_all)
        self.setStyleSheet(f"background: {bg};")