from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
from pages.components.bottom_nav import BottomNav
from .components.fab import FABButton
from .components.goal_card import GoalCard
from .components.habit_card import HabitCard
from .components.progress_card import ProgressCard
from .components.section_header import SectionHeader
from .components.modal import NewHabitModal
from .components.delete_modals import DeleteConfirmModal, DeleteSuccessModal

from pages.utils.helpers import check_streak_generator
from pages.constants import APP_FONT, BG, BORDER, ORANGE, TEXT_D, TEXT_M, WHITE
import datetime


class HomePage(QMainWindow):
    NAV_H = 56
    see_all_habits = Signal()
    see_all_goals = Signal()
    nav_requested = Signal(str)

    create_habit_requested = Signal(str, str, int, str)
    refresh_requested = Signal()
    delete_habit_requested = Signal(str)
    update_habit_requested = Signal(str, str, str, int, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker")
        self.setFixedSize(390, 780)

        self.user = None

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet(f"background: {BG};")

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scrollable content area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{ background: {BG}; border: none; }}
            QScrollBar:vertical {{
                background: {BG};
                width: 4px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER};
                border-radius: 2px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet(f"background: {BG};")
        self.scroll.setWidget(self.content_widget)

        main_layout.addWidget(self.scroll)

        # Divider line above nav
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background: {BORDER};")
        main_layout.addWidget(div)

        # Bottom nav
        self.nav = BottomNav(active_tab="Home")
        self.nav.tab_requested.connect(self._on_nav_clicked)
        main_layout.addWidget(self.nav)

        # Build page content
        self._build_page()

        # FAB
        self.fab = FABButton(self)
        self._reposition_fab()
        self.fab.clicked.connect(self._open_modal)

    def _reposition_fab(self):
        self.fab.move(390 - 72, 780 - self.NAV_H - 72)

    def _build_page(self):
        # Clear existing layout
        if self.content_widget.layout():
            QWidget().setLayout(self.content_widget.layout())

        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(16, 26, 16, 16)
        layout.setSpacing(0)

        today = datetime.date.today()

        # Date
        try:
            day_str = today.strftime("%-d %B %Y")
            day_str = today.strftime("%a, ") + day_str
        except ValueError:
            day_str = today.strftime("%a, %d %B %Y")

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setSpacing(0)

        date_lbl = QLabel(day_str)
        date_lbl.setFont(QFont(APP_FONT, 11))
        date_lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
        top_bar_layout.addWidget(date_lbl)

        top_bar_layout.addStretch()

        # Streak
        completed_dates = set()
        if self.user:
            completed_dates = set(self.user.get("all_completed_dates", []))

        habit_history = []
        check_date = today

        if str(check_date) not in completed_dates:
            check_date -= datetime.timedelta(days=1)

        while True:
            is_completed = str(check_date) in completed_dates
            habit_history.append({"is_completed": is_completed})
            if not is_completed:
                break
            check_date -= datetime.timedelta(days=1)

        streak_count = sum(1 for _ in check_streak_generator(habit_history))

        streak_lbl = QLabel(f"🔥 {streak_count}")
        streak_lbl.setFont(QFont(APP_FONT, 12, QFont.Bold))
        streak_lbl.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        top_bar_layout.addWidget(streak_lbl)

        layout.addLayout(top_bar_layout)

        layout.addSpacing(4)

        # Greeting
        hello_row = QHBoxLayout()
        hello_row.setSpacing(0)
        hello_prefix = QLabel("Hello, ")
        hello_prefix.setFont(QFont(APP_FONT, 26, QFont.Bold))
        hello_prefix.setStyleSheet(f"color: {TEXT_D}; background: transparent;")

        name = self.user.get("name", "User") if self.user else "User"
        self.hello_name = QLabel(name + "!")
        self.hello_name.setFont(QFont(APP_FONT, 26, QFont.Bold))
        self.hello_name.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        self.hello_name.setWordWrap(True)

        hello_row.addWidget(hello_prefix)
        hello_row.addWidget(self.hello_name)
        hello_row.addStretch()
        layout.addLayout(hello_row)

        layout.addSpacing(16)

        # Progress Card
        self.progress_card = ProgressCard()
        habits_all = self.user.get("today_habits", []) if self.user else []
        self.progress_card.set_habits(habits_all)
        layout.addWidget(self.progress_card)

        layout.addSpacing(16)

        # Today Habit
        habits_container = QWidget()
        habits_container.setStyleSheet(f"""
            QWidget {{
                background: {WHITE};
                border-radius: 16px;
            }}
        """)

        habits_layout = QVBoxLayout(habits_container)
        habits_layout.setContentsMargins(12, 8, 12, 12)
        habits_layout.setSpacing(8)

        habits_header = SectionHeader(
            "Today Habits",
            "See all",
            bg=WHITE,
            on_action=lambda: self.see_all_habits.emit(),
        )
        habits_layout.addWidget(habits_header)

        habits = self.user.get("today_habits", []) if self.user else []
        if not habits:
            empty_habits_lbl = QLabel("No habits for today")
            empty_habits_lbl.setFont(QFont(APP_FONT, 14))
            empty_habits_lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
            empty_habits_lbl.setAlignment(Qt.AlignCenter)
            habits_layout.addSpacing(10)
            habits_layout.addWidget(empty_habits_lbl)
            habits_layout.addSpacing(10)
        else:
            for h in habits:
                hc = HabitCard(h)
                hc.habit_toggled.connect(self._on_habit_toggled)
                hc.edit_requested.connect(self._open_edit_modal)
                hc.delete_requested.connect(
                    lambda habit_dict=h: self._open_delete_confirm(habit_dict["id"])
                )
                habits_layout.addWidget(hc)

        layout.addWidget(habits_container)
        layout.addSpacing(16)

        # Your Goals
        goals_container = QWidget()
        goals_container.setStyleSheet(f"""
            QWidget {{
                background: {WHITE};
                border-radius: 16px;
            }}
        """)

        goals_layout = QVBoxLayout(goals_container)
        goals_layout.setContentsMargins(12, 8, 12, 12)
        goals_layout.setSpacing(8)

        goals_header = SectionHeader(
            "Your Goals",
            "See all",
            bg=WHITE,
            on_action=lambda: self.see_all_goals.emit(),
        )
        goals_layout.addWidget(goals_header)

        goals = (self.user.get("goals", []) if self.user else [])[:3]
        if not goals:
            empty_goals_lbl = QLabel("No goals added yet")
            empty_goals_lbl.setFont(QFont(APP_FONT, 14))
            empty_goals_lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
            empty_goals_lbl.setAlignment(Qt.AlignCenter)
            goals_layout.addSpacing(10)
            goals_layout.addWidget(empty_goals_lbl)
            goals_layout.addSpacing(10)
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

                goals_layout.addWidget(gc)

        layout.addWidget(goals_container)

        # Spacer at bottom for FAB clearance
        layout.addSpacing(10)
        layout.addStretch()

    def set_user(self, session: dict):
        self.user = session
        self._build_page()

    def _open_modal(self):
        self.modal = NewHabitModal(self.window())
        self.modal.habit_submitted.connect(self.create_habit_requested.emit)

    def _open_edit_modal(self, habit: dict):
        self.modal = NewHabitModal(self.window(), habit=habit)
        self.modal.habit_updated.connect(self.update_habit_requested.emit)

    def _open_delete_confirm(self, habit_id: str):
        self.del_confirm = DeleteConfirmModal(self.window())
        self.del_confirm.confirm_delete.connect(
            lambda: self._on_confirmed_delete(habit_id)
        )

    def _on_confirmed_delete(self, habit_id: str):
        self.delete_habit_requested.emit(habit_id)
        self.del_success = DeleteSuccessModal(self.window())

    def _on_habit_toggled(self):
        self.refresh_requested.emit()

    def _on_nav_clicked(self, tab_name):
        self.nav_requested.emit(tab_name)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "modal") and self.modal.isVisible():
            self.modal.setGeometry(0, 0, self.width(), self.height())
        self._reposition_fab()
