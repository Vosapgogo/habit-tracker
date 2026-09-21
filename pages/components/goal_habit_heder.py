import os
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from pages.constants import APP_FONT, ORANGE, TEXT_D

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GoalHabitHeader(QWidget):
    go_back = Signal()

    def __init__(self, title_text: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        back_btn = QPushButton("←")
        back_btn.setFixedSize(36, 36)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_D};
                font-size: 20px;
                border: none;
            }}
            QPushButton:hover {{ color: {ORANGE}; }}
        """)
        back_btn.clicked.connect(self.go_back.emit)

        title_lbl = QLabel(title_text)
        title_lbl.setFont(QFont(APP_FONT, 18, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        title_lbl.setWordWrap(True)

        layout.addWidget(back_btn)
        layout.addWidget(title_lbl)
        layout.addStretch()
