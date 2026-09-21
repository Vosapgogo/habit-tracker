from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt
from pages.constants import APP_FONT, WHITE


class FABButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("+", parent)
        self.setFixedSize(56, 56)
        self.setFont(QFont(APP_FONT, 26, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: #26C281;
                color: {WHITE};
                border-radius: 28px;
                border: none;
                padding-bottom: 4px;
            }}
            QPushButton:hover {{
                background: #32D891;
            }}
            QPushButton:pressed {{
                background: #1EA86E;
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
