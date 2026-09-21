from PySide6.QtWidgets import QFrame, QLabel, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal

from pages.components.goal_habit_heder import GoalHabitHeader
from pages.components.primary_button import PrimaryButton
from pages.components.form_input import FormInputField

from pages.constants import APP_FONT
from pages.utils.errors import ValidationError

from pages.utils.helpers import (
    prevent_double_click,
    strip_whitespaces,
    validate_account_data,
)


class AccountPage(QWidget):
    go_settings = Signal()

    update_account_requested = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; } QScrollBar:vertical { width: 0px; background: transparent; }"
        )

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 20, 16, 16)

        header = GoalHabitHeader("Account")
        header.go_back.connect(self.go_settings.emit)
        layout.addWidget(header)

        fields = [
            ("Name", False),
            ("Email", False),
            ("Password", True),
            ("Password Confirmation", True),
        ]

        self.inputs = {}

        for label, is_pass in fields:
            field_widget = FormInputField(label_text=label, is_password=is_pass)
            layout.addWidget(field_widget)
            layout.addSpacing(15)
            self.inputs[label] = field_widget

        self.error_lbl = QLabel("")
        self.error_lbl.setFont(QFont(APP_FONT, 11))
        self.error_lbl.setStyleSheet("color: #E53935; background: transparent;")
        self.error_lbl.setAlignment(Qt.AlignCenter)
        self.error_lbl.setWordWrap(True)
        layout.addWidget(self.error_lbl)
        layout.addSpacing(10)

        update_btn = PrimaryButton("Update")
        update_btn.clicked.connect(self._on_update_clicked)

        layout.addWidget(update_btn)
        layout.addStretch()

    def set_user(self, session):
        self.user = session
        if self.user:
            self.inputs["Name"].entry.setText(self.user.get("name", ""))
            self.inputs["Email"].entry.setText(self.user.get("email", ""))

            self.inputs["Password"].entry.setText("")
            self.inputs["Password Confirmation"].entry.setText("")

            self.inputs["Password"].entry.setPlaceholderText("Leave blank to keep old")
            self.inputs["Password Confirmation"].entry.setPlaceholderText(
                "Leave blank to keep old"
            )

            self.error_lbl.setText("")

    def _on_update_clicked(self):
        name = self.inputs["Name"].text()
        email = self.inputs["Email"].text()
        pwd = self.inputs["Password"].text()
        pwd2 = self.inputs["Password Confirmation"].text()

        self._process_update(name, email, pwd, pwd2)

    @prevent_double_click(delay=1.5)
    @strip_whitespaces
    def _process_update(self, name, email, pwd, pwd2):
        try:
            if not pwd and not pwd2:
                validate_account_data(name, email, "ValidPass123!", "ValidPass123!")
                pwd = ""
            else:
                validate_account_data(name, email, pwd, pwd2)
        except ValidationError as e:
            self.error_lbl.setText(str(e))
            return

        self.error_lbl.setText("")
        self.update_account_requested.emit(name, email, pwd)
