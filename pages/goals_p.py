import os

from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from pages.components.modal import NewHabitModal
from .constants import APP_FONT, BG, ORANGE, TEXT_D, TEXT_M, WHITE
from .components.goal_card import GoalCard
from pages.components.delete_modals import DeleteConfirmModal, DeleteSuccessModal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class GoalsPageHome(QWidget):
    go_home = Signal()
    refresh_requested = Signal()

    update_habit_requested = Signal(str, str, str, int, str)
    delete_habit_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.user = None
        self._goals = []
        self._filter = "All"
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
        header = QHBoxLayout()
        header.setSpacing(0)

        back_btn = QPushButton("←")
        back_btn.setFixedSize(36, 36)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_D};
                font-size: 20px;
                border: none;
            }}
            QPushButton:hover {{ color: {ORANGE}; }}
        """)
        back_btn.clicked.connect(self.go_back_home)

        title_lbl = QLabel("Your Goals")
        title_lbl.setFont(QFont(APP_FONT, 20, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        title_lbl.setWordWrap(True)

        header.addWidget(back_btn)
        header.addSpacing(8)
        header.addWidget(title_lbl)
        header.addStretch()

        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Everyday", "Weekdays", "Weekends"])
        self.filter_combo.setCurrentText(self._filter)
        self.filter_combo.setFixedHeight(34)
        self.filter_combo.setMinimumWidth(110)
        self.filter_combo.setCursor(Qt.PointingHandCursor)
        self.filter_combo.setFont(QFont(APP_FONT, 13))

        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                background: #E8E8E8; color: {TEXT_D};
                border-radius: 6px; padding: 4px 10px;
            }}
            QComboBox::drop-down {{ border: none; width: 26px; }}
        """)

        self.filter_combo.currentTextChanged.connect(self._apply_filter)
        header.addWidget(self.filter_combo)

        container_layout.addLayout(header)

        # Goals cards
        goals = self._goals
        if self._filter != "All":
            goals = [g for g in goals if g.get("type") == self._filter]

        if not goals:
            empty_lbl = QLabel("No goals for this filter")
            empty_lbl.setFont(QFont(APP_FONT, 14))
            empty_lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
            empty_lbl.setAlignment(Qt.AlignCenter)
            container_layout.addSpacing(20)
            container_layout.addWidget(empty_lbl)
            container_layout.addSpacing(20)
        else:
            for g in goals:
                card_data = {
                    "name": g["goal"],
                    "progress": g["progress"],
                    "target": f"{g['done_count']} from {g['total_days']} days target",
                    "type": g["type"],
                    "id": g.get("habit_id"),
                    "habit_name": g.get("habit_name"),
                }
                gc = GoalCard(card_data)

                gc.edit_requested.connect(
                    lambda g_dict=card_data: self._open_edit_modal(
                        {"id": g_dict["id"], "name": g_dict["habit_name"]}
                    )
                )
                gc.delete_requested.connect(
                    lambda g_dict=card_data: self._open_delete_confirm(g_dict["id"])
                )

                container_layout.addWidget(gc)

        layout.addWidget(container)
        layout.addStretch()

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

    def go_back_home(self):
        self.go_home.emit()

    def _apply_filter(self, option):
        self._filter = option
        self._build()

    def set_specific_goals(self, goals):
        self._goals = goals
        self._build()

    def set_user(self, session):
        self.user = session
        self._goals = session.get("goals", [])
        self._build()
