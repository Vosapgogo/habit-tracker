from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from pages.constants import WHITE, ORANGE, ORANGE_L, BG, TEXT_D, TEXT_M, TEXT_L, BORDER
from models.user_session import login_user


class LoginPage(QWidget):
    """Log In screen"""

    go_signup = Signal()       # switch to Sign Up
    go_home   = Signal()       # login success → go to main app

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

        title = QLabel("Log In")
        title.setFont(QFont("Helvetica Neue", 28, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_D}; background: transparent;")

        signup_row = QHBoxLayout()
        signup_row.setSpacing(2)
        signup_lbl = QLabel("Sign Up")
        signup_lbl.setFont(QFont("Helvetica Neue", 13, QFont.Bold))
        signup_lbl.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        signup_lbl.setCursor(Qt.PointingHandCursor)
        signup_lbl.mousePressEvent = lambda e: self.go_signup.emit()
        arrow = QLabel("›")
        arrow.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
        arrow.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        signup_row.addWidget(signup_lbl)
        signup_row.addWidget(arrow)

        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addLayout(signup_row)
        layout.addLayout(header_row)

        layout.addSpacing(32)

        # ── Fields ───────────────────────────────────────────────────────────
        self.email_input = self._make_field(layout, "Email")
        self.pass_input  = self._make_field(layout, "Password", password=True)

        # ── Remember me + Forgot password ────────────────────────────────────
        row = QHBoxLayout()
        self.remember_cb = QCheckBox("Remember me")
        self.remember_cb.setFont(QFont("Helvetica Neue", 12))
        self.remember_cb.setStyleSheet(f"""
            QCheckBox {{ color: {TEXT_M}; background: transparent; }}
            QCheckBox::indicator {{
                width: 16px; height: 16px;
                border: 1px solid {BORDER};
                border-radius: 3px;
                background: {WHITE};
            }}
            QCheckBox::indicator:checked {{
                background: {ORANGE};
                border: 1px solid {ORANGE};
            }}
        """)
        forgot = QLabel("Forgot Password?")
        forgot.setFont(QFont("Helvetica Neue", 12, QFont.Bold))
        forgot.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        forgot.setCursor(Qt.PointingHandCursor)

        row.addWidget(self.remember_cb)
        row.addStretch()
        row.addWidget(forgot)
        layout.addLayout(row)

        layout.addSpacing(8)

        # ── Error label ──────────────────────────────────────────────────────
        self.error_lbl = QLabel("")
        self.error_lbl.setFont(QFont("Helvetica Neue", 11))
        self.error_lbl.setStyleSheet("color: #E53935; background: transparent;")
        self.error_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_lbl)

        layout.addSpacing(16)

        # ── Log In button ────────────────────────────────────────────────────
        btn = QPushButton("Log In")
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

        layout.addSpacing(24)

        # ── Or log in with ───────────────────────────────────────────────────
        or_lbl = QLabel("Or log in with:")
        or_lbl.setFont(QFont("Helvetica Neue", 12))
        or_lbl.setAlignment(Qt.AlignCenter)
        or_lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
        layout.addWidget(or_lbl)

        layout.addSpacing(10)

        google_btn = QPushButton("  G")
        google_btn.setFixedHeight(48)
        google_btn.setFont(QFont("Helvetica Neue", 16, QFont.Bold))
        google_btn.setCursor(Qt.PointingHandCursor)
        google_btn.setStyleSheet(f"""
            QPushButton {{
                background: {WHITE};
                color: #4285F4;
                border: 1px solid {BORDER};
                border-radius: 10px;
            }}
            QPushButton:hover {{ background: #F5F5F5; }}
        """)
        layout.addWidget(google_btn)

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
        email = self.email_input.text().strip()
        pwd   = self.pass_input.text()

        if not email:
            self.error_lbl.setText("Please enter your email")
            return
        if not pwd:
            self.error_lbl.setText("Please enter your password")
            return

        success, msg = login_user(email, pwd)
        if not success:
            self.error_lbl.setText(msg)
            return

        self.error_lbl.setText("")
        self.go_home.emit()