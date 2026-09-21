from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from pages.constants import APP_FONT, ORANGE, BG, TEXT_D

from pages.components.form_input import FormInputField
from pages.components.primary_button import PrimaryButton

from models.user_session import login_user

from pages.utils.errors import ValidationError

from pages.utils.helpers import (
    prevent_double_click,
    strip_whitespaces,
    validate_account_data,
)


class LoginPage(QWidget):
    go_signup = Signal()
    go_home = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background: {BG};")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 32)

        # Header row
        header_row = QHBoxLayout()

        title = QLabel("Log In")
        title.setFont(QFont(APP_FONT, 28, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_D}; background: transparent;")

        signup_lbl = QLabel("Sign Up ›")
        signup_lbl.setFont(QFont(APP_FONT, 13, QFont.Bold))
        signup_lbl.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        signup_lbl.setCursor(Qt.PointingHandCursor)
        signup_lbl.mousePressEvent = lambda e: self.go_signup.emit()

        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addWidget(signup_lbl)
        layout.addLayout(header_row)

        layout.addSpacing(32)

        # Fields
        self.email_input = FormInputField("Email")
        self.pwd_input = FormInputField("Password", is_password=True)
        layout.addWidget(self.email_input)
        layout.addSpacing(14)
        layout.addWidget(self.pwd_input)
        layout.addSpacing(8)

        # Error label
        self.error_lbl = QLabel("")
        self.error_lbl.setFont(QFont(APP_FONT, 11))
        self.error_lbl.setStyleSheet("color: #E53935; background: transparent;")
        self.error_lbl.setAlignment(Qt.AlignCenter)
        self.error_lbl.setWordWrap(True)
        layout.addWidget(self.error_lbl)

        layout.addSpacing(16)

        # Log In button
        btn = PrimaryButton("Log In")
        btn.clicked.connect(self._submit)
        layout.addWidget(btn)

        layout.addStretch()

    def _submit(self):
        email = self.email_input.text()
        pwd = self.pwd_input.text()

        self._process_login(email, pwd)

    @prevent_double_click(delay=1.5)
    @strip_whitespaces
    def _process_login(self, email, pwd):
        try:
            validate_account_data(email=email, pwd=pwd)
            login_user(email, pwd)
        except ValidationError as e:
            self.error_lbl.setText(str(e))
            return

        self.error_lbl.setText("")
        self.go_home.emit()

    def clear_fields(self):
        self.email_input.clear()
        self.pwd_input.clear()
        self.error_lbl.setText("")
