import os
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)
from PySide6.QtGui import QFont, Qt, QIcon
from PySide6.QtCore import QSize
from pages.constants import APP_FONT, ORANGE, WHITE, TEXT_D, TEXT_M, BORDER

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_eye = os.path.join(BASE_DIR, "images", "eye.png")
path_closed_eye = os.path.join(BASE_DIR, "images", "closed_eye.png")


class FormInputField(QWidget):
    def __init__(self, label_text, is_password: bool = False, parent=None):
        super().__init__(parent)

        self.is_password = is_password
        self._password_visible = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Label
        lbl = QLabel(label_text)
        lbl.setFont(QFont(APP_FONT, 12))
        lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        self.entry = QLineEdit()
        self.entry.setMinimumHeight(46)

        self.entry.setFont(QFont(APP_FONT, 13))

        pad_right = 40 if is_password else 14

        self.entry.setStyleSheet(f"""
            QLineEdit {{
                background: {WHITE};
                border: 1px solid {BORDER};
                border-radius: 10px;
                padding: 0 {pad_right}px 0 14px;
                color: {TEXT_D};
            }}
            QLineEdit:focus {{
                border: 1.5px solid {ORANGE};
            }}
        """)

        if self.is_password:
            self.entry.setEchoMode(QLineEdit.EchoMode.Password)

            self.toggle_btn = QPushButton()
            self.toggle_btn.setCursor(Qt.PointingHandCursor)
            self.toggle_btn.setFocusPolicy(Qt.NoFocus)

            self.toggle_btn.setIcon(QIcon(path_eye))
            self.toggle_btn.setIconSize(QSize(20, 20))

            self.toggle_btn.setStyleSheet("background: transparent; border: none;")
            self.toggle_btn.clicked.connect(self._toggle_visibility)

            entry_layout = QHBoxLayout(self.entry)
            entry_layout.setContentsMargins(0, 0, 10, 0)
            entry_layout.addWidget(
                self.toggle_btn, alignment=Qt.AlignRight | Qt.AlignVCenter
            )

        layout.addWidget(self.entry)

    def _toggle_visibility(self):
        self._password_visible = not self._password_visible
        if self._password_visible:
            self.entry.setEchoMode(QLineEdit.Normal)
            self.toggle_btn.setIcon(QIcon(path_closed_eye))
        else:
            self.entry.setEchoMode(QLineEdit.Password)
            self.toggle_btn.setIcon(QIcon(path_eye))

    def text(self):
        return self.entry.text()

    def clear(self):
        self.entry.clear()
