from PySide6.QtWidgets import (
    QLabel,
    QScrollArea,
    QFrame,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
from pages.constants import APP_FONT, TEXT_D, TEXT_M, WHITE

from pages.components.bottom_nav import BottomNav
from pages.components.log_out_modals import LogoutConfirmModal, LogoutSuccessModal
from pages.components.delete_account_modals import (
    DeleteAccountConfirmModal,
    DeleteAccountSuccessModal,
)


class SettingsPage(QWidget):
    go_account = Signal()
    nav_requested = Signal(str)
    go_welcome = Signal()
    delete_account_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

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

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 26, 16, 16)

        title = QLabel("Settings")
        title.setFont(QFont(APP_FONT, 28, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_D};")
        content_layout.addWidget(title)
        content_layout.addSpacing(20)

        container = QWidget()
        container.setStyleSheet(f"background: {WHITE}; border-radius: 16px;")
        cont_layout = QVBoxLayout(container)

        items = ["Account", "Log Out", "Delete"]
        for name in items:
            btn = QPushButton()
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: #F8F8F8; 
                    border-radius: 8px; 
                    border: none;
                }}
            """)

            if name == "Account":
                btn.clicked.connect(self.go_account.emit)
            elif name == "Log Out":
                btn.clicked.connect(self._open_logout_confirm)
            elif name == "Delete":
                btn.clicked.connect(self._open_delete_account_confirm)

            btn_layout = QHBoxLayout(btn)
            btn_layout.setContentsMargins(15, 0, 15, 0)

            name_lbl = QLabel(name)
            name_lbl.setStyleSheet(
                f"color: {TEXT_D}; font-size: 16px; background: transparent;"
            )
            name_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)

            arrow_lbl = QLabel("›")
            arrow_lbl.setStyleSheet(
                f"color: {TEXT_M}; font-size: 20px; background: transparent;"
            )
            arrow_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)

            btn_layout.addWidget(name_lbl)
            btn_layout.addStretch()
            btn_layout.addWidget(arrow_lbl)

            cont_layout.addWidget(btn)
            cont_layout.addSpacing(8)

        content_layout.addWidget(container)
        content_layout.addStretch()

        layout.addWidget(scroll)

        self.nav = BottomNav(active_tab="Setting")
        self.nav.tab_requested.connect(self._on_nav_clicked)
        layout.addWidget(self.nav)

    def _on_nav_clicked(self, tab_name):
        self.nav_requested.emit(tab_name)

    def _open_logout_confirm(self):
        self.logout_confirm = LogoutConfirmModal(self.window())
        self.logout_confirm.confirm_logout.connect(self._on_confirmed_logout)

    def _on_confirmed_logout(self):
        self.logout_success = LogoutSuccessModal(self.window())
        self.logout_success.success_ok.connect(self._on_success_ok)

    def _open_delete_account_confirm(self):
        self.delete_acc_confirm = DeleteAccountConfirmModal(self.window())
        self.delete_acc_confirm.confirm_delete.connect(self._on_confirmed_delete_acc)

    def _on_confirmed_delete_acc(self):
        self.delete_account_requested.emit()
        self.delete_acc_success = DeleteAccountSuccessModal(self.window())
        self.delete_acc_success.success_ok.connect(self._on_success_ok)

    def _on_success_ok(self):
        self.go_welcome.emit()
