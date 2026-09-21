from PySide6.QtWidgets import QFrame, QScrollArea, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from pages.components.goal_habit_heder import GoalHabitHeader
from pages.components.habit_card import HabitCard
from pages.components.modal import NewHabitModal
from pages.components.delete_modals import DeleteConfirmModal, DeleteSuccessModal
from .constants import APP_FONT, BG, TEXT_M, WHITE

import os
from PySide6.QtGui import QFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class HabitsPage(QWidget):
    go_home = Signal()
    refresh_requested = Signal()

    update_habit_requested = Signal(str, str, str, int, str)
    delete_habit_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.user = None
        self.setStyleSheet(f"background: {BG};")
        self._build()

    def _build(self):
        for child in self.findChildren(QWidget):
            child.setParent(None)
            child.deleteLater()
        if self.layout():
            QWidget().setLayout(self.layout())

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
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # White container
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {WHITE};
                border-radius: 16px;
            }}
        """)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(8)

        # Title
        header = GoalHabitHeader("Your Habits")
        header.go_back.connect(self.go_home.emit)
        container_layout.addWidget(header)

        # Habit cards
        habits = self.user.get("habits", []) if self.user else []
        if not habits:
            empty_lbl = QLabel("You have no habits yet")
            empty_lbl.setFont(QFont(APP_FONT, 14))
            empty_lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
            empty_lbl.setAlignment(Qt.AlignCenter)
            container_layout.addSpacing(20)
            container_layout.addWidget(empty_lbl)
            container_layout.addSpacing(20)
        else:
            for h in habits:
                hc = HabitCard(h)
                hc.habit_toggled.connect(self._on_habit_toggled)
                hc.edit_requested.connect(self._open_edit_modal)
                hc.delete_requested.connect(
                    lambda habit_dict=h: self._open_delete_confirm(habit_dict["id"])
                )
                container_layout.addWidget(hc)

        layout.addWidget(container)
        layout.addStretch()

    def _on_habit_toggled(self):
        self.refresh_requested.emit()

    def _open_edit_modal(self, habit):
        self.modal = NewHabitModal(self, habit=habit)
        self.modal.habit_updated.connect(self.update_habit_requested.emit)

    def _open_delete_confirm(self, habit_id):
        self.del_confirm = DeleteConfirmModal(self.window())
        self.del_confirm.confirm_delete.connect(
            lambda: self._on_confirmed_delete(habit_id)
        )

    def _on_confirmed_delete(self, habit_id):
        self.delete_habit_requested.emit(habit_id)
        self.del_success = DeleteSuccessModal(self.window())

    def set_user(self, session):
        self.user = session
        self._build()
