from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from pages.constants import APP_FONT, ORANGE, BG, TEXT_D

from pages.components.form_input import FormInputField
from pages.components.primary_button import PrimaryButton

from pages.utils.errors import ValidationError

from models.user_session import register_user
from pages.utils.helpers import (
    prevent_double_click,
    strip_whitespaces,
    validate_account_data,
)


class SignUpPage(QWidget):
    go_login = Signal()
    go_success = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background: {BG};")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 32)
        layout.setSpacing(0)

        # Header row
        header_row = QHBoxLayout()

        title = QLabel("Sign Up")
        title.setFont(QFont(APP_FONT, 28, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_D}; background: transparent;")

        login_lbl = QLabel("Log In ›")
        login_lbl.setFont(QFont(APP_FONT, 13, QFont.Bold))
        login_lbl.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        login_lbl.setCursor(Qt.PointingHandCursor)
        login_lbl.mousePressEvent = lambda e: self.go_login.emit()

        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addWidget(login_lbl)
        layout.addLayout(header_row)

        layout.addSpacing(32)

        # Fields
        self.name_input = FormInputField("Name")
        self.email_input = FormInputField("Email")
        self.pwd_input = FormInputField("Password", is_password=True)
        self.pwd2_input = FormInputField("Password Confirmation", is_password=True)

        layout.addWidget(self.name_input)
        layout.addSpacing(14)
        layout.addWidget(self.email_input)
        layout.addSpacing(14)
        layout.addWidget(self.pwd_input)
        layout.addSpacing(14)
        layout.addWidget(self.pwd2_input)

        layout.addSpacing(8)

        # Error label
        self.error_lbl = QLabel("")
        self.error_lbl.setFont(QFont(APP_FONT, 11))
        self.error_lbl.setStyleSheet("color: #E53935; background: transparent;")
        self.error_lbl.setAlignment(Qt.AlignCenter)
        self.error_lbl.setWordWrap(True)
        layout.addWidget(self.error_lbl)

        layout.addSpacing(16)

        # Sign Up button
        btn = PrimaryButton("Sign Up")
        btn.clicked.connect(self._submit)
        layout.addWidget(btn)

        layout.addStretch()

    def _submit(self):
        name = self.name_input.text()
        email = self.email_input.text()
        pwd = self.pwd_input.text()
        pwd2 = self.pwd2_input.text()

        self._process_signup(name, email, pwd, pwd2)

    @prevent_double_click(delay=1.5)
    @strip_whitespaces
    def _process_signup(self, name, email, pwd, pwd2):
        try:
            validate_account_data(name, email, pwd, pwd2)
            register_user(name, email, pwd)
        except ValidationError as e:
            self.error_lbl.setText(str(e))
            return

        self.error_lbl.setText("")
        self.go_success.emit(name)

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.pwd_input.clear()
        self.pwd2_input.clear()
        self.error_lbl.setText("")
