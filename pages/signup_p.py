from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from pages.constants import WHITE, ORANGE, ORANGE_L, BG, TEXT_D, TEXT_M, TEXT_L, BORDER
from models.user_session import register_user

import re

class SignUpPage(QWidget):
    """Sign Up screen"""

    go_login   = Signal()          # switch to Log In
    go_success = Signal(str)       # registration done → pass name

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background: {BG};")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 48, 32, 32)
        layout.setSpacing(0)

        # ── Header row ───────────────────────────────────────────────────────
        header_row = QHBoxLayout()

        title = QLabel("Sign Up")
        title.setFont(QFont("Helvetica Neue", 28, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_D}; background: transparent;")

        login_row = QHBoxLayout()
        login_row.setSpacing(2)
        login_lbl = QLabel("Log In")
        login_lbl.setFont(QFont("Helvetica Neue", 13, QFont.Bold))
        login_lbl.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        login_lbl.setCursor(Qt.PointingHandCursor)
        login_lbl.mousePressEvent = lambda e: self.go_login.emit()
        arrow = QLabel("›")
        arrow.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
        arrow.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        login_row.addWidget(login_lbl)
        login_row.addWidget(arrow)

        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addLayout(login_row)
        layout.addLayout(header_row)

        layout.addSpacing(32)

        # ── Fields ───────────────────────────────────────────────────────────
        self.name_input  = self._make_field(layout, "Name")
        self.email_input = self._make_field(layout, "Email")
        self.pass_input  = self._make_field(layout, "Password", password=True)
        self.pass2_input = self._make_field(layout, "Password Confirmation", password=True)

        layout.addSpacing(8)

        # ── Error label ──────────────────────────────────────────────────────
        self.error_lbl = QLabel("")
        self.error_lbl.setFont(QFont("Helvetica Neue", 11))
        self.error_lbl.setStyleSheet("color: #E53935; background: transparent;")
        self.error_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_lbl)

        layout.addSpacing(16)

        # ── Sign Up button ───────────────────────────────────────────────────
        btn = QPushButton("Sign Up")
        btn.setFixedHeight(52)
        btn.setFont(QFont("Helvetica Neue", 15, QFont.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ORANGE}, stop:1 {ORANGE_L});
                color: {WHITE};
                border-radius: 26px;
                border: none;
            }}
            QPushButton:hover {{ background: {ORANGE_L}; }}
            QPushButton:pressed {{ background: #E05010; }}
        """)
        btn.clicked.connect(self._submit)
        layout.addWidget(btn)

        layout.addStretch()

    def _make_field(self, layout, label_text: str, password=False) -> QLineEdit:
        lbl = QLabel(label_text)
        lbl.setFont(QFont("Helvetica Neue", 12))
        lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
        layout.addWidget(lbl)
        layout.addSpacing(4)

        entry = QLineEdit()
        entry.setFixedHeight(46)
        entry.setFont(QFont("Helvetica Neue", 13))
        if password:
            entry.setEchoMode(QLineEdit.Password)
        entry.setStyleSheet(f"""
            QLineEdit {{
                background: {WHITE};
                border: 1px solid {BORDER};
                border-radius: 10px;
                padding: 0 14px;
                color: {TEXT_D};
            }}
            QLineEdit:focus {{
                border: 1.5px solid {ORANGE};
            }}
        """)
        layout.addWidget(entry)
        layout.addSpacing(14)
        return entry

    def _submit(self):
        name  = self.name_input.text().strip()
        email = self.email_input.text().strip()
        pwd   = self.pass_input.text()
        pwd2  = self.pass2_input.text()

        if not name:
            self.error_lbl.setText("Please enter your name")
            return
        if not email or "@gmail.com" not in email:
            self.error_lbl.setText("Please enter a valid email")
            return
        if len(pwd) < 6:
            self.error_lbl.setText("Password must be at least 6 characters")
            return
        if not re.match(r".*[A-Za-z].*", pwd):
            self.error_lbl.setText("Password must contain at least 1 letter")
            return
        if not re.match(r".*\d.*", pwd):
            self.error_lbl.setText("Password must contain at least 1 number")
            return
        if pwd != pwd2:
            self.error_lbl.setText("Passwords do not match")
            return

        success, msg = register_user(name, email, pwd)
        if not success:
            self.error_lbl.setText(msg)
            return

        self.error_lbl.setText("")
        self.go_success.emit(name)