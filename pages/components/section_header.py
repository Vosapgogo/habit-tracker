from PySide6.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from pages.constants import APP_FONT, ORANGE, TEXT_D, WHITE


class SectionHeader(QWidget):
    def __init__(self, title, action_text="", bg=WHITE, on_action=None):
        super().__init__()
        self.on_action = on_action
        self.setMinimumHeight(36)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(title)
        title_label.setFont(QFont(APP_FONT, 15, QFont.Bold))
        title_label.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        title_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addStretch()

        if action_text:
            see_all = QLabel(action_text)
            see_all.setStyleSheet(f"color: {ORANGE}; background: transparent;")
            see_all.setCursor(Qt.PointingHandCursor)

            see_all.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

            see_all.mousePressEvent = lambda e: (
                self.on_action() if self.on_action else None
            )
            layout.addWidget(see_all)

        self.setStyleSheet(f"background: {bg};")
