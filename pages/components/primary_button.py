from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from pages.constants import APP_FONT, ORANGE, ORANGE_L, WHITE


class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(52)

        self.setFont(QFont(APP_FONT, 15, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ORANGE}, stop:1 {ORANGE_L});
                color: {WHITE};
                border-radius: 14px;
                border: none;
            }}
            QPushButton:hover {{ background: {ORANGE_L}; }}
            QPushButton:pressed {{ background: #E05010; }}
        """)
