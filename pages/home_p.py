from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.components.bottom_nav import BottomNav
from .components.fab import FABButton
from .components.goal_card import GoalCard
from .components.habit_card import HabitsCard
from .components.progress_card import ProgressCard
from .components.section_header import SectionHeader
from .components.modal import NewHabitModal

from pages.utils.helpers import *
from pages.constants import *
import datetime

HABITS = [
    {"name": "Meditating",       "done": True},
    {"name": "Read Philosophy",  "done": True},
    {"name": "Journaling",       "done": False},
]

GOALS = [
    {"name": "Finish 5 Philosophy Books",  "progress": 0.71, "target": "5 from 7 days target", "type": "Everyday"},
    {"name": "Sleep before 11 pm",         "progress": 0.71, "target": "5 from 7 days target", "type": "Everyday"},
    {"name": "Finish read The Hobbits",    "progress": 0.50, "target": "3 from 6 days target", "type": "Everyday"},
]

TODAY = datetime.date.today()

class HomePage(QMainWindow):
    NAV_H = 56

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
        self.nav = BottomNav()
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
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(0)

        # ── Date + Greeting ──────────────────────────────────────────────────
        try:
            day_str = TODAY.strftime("%-d %B %Y")
            day_str = TODAY.strftime("%a, ") + day_str
        except ValueError:
            day_str = TODAY.strftime("%a, %d %B %Y")

        date_lbl = QLabel(day_str)
        date_lbl.setFont(QFont("Helvetica Neue", 11))
        date_lbl.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
        layout.addWidget(date_lbl)

        layout.addSpacing(4)

        hello_row = QHBoxLayout()
        hello_row.setSpacing(0)
        hello_prefix = QLabel("Hello, ")
        hello_prefix.setFont(QFont("Helvetica Neue", 26, QFont.Bold))
        hello_prefix.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        name = self.user.get("name", "User") if self.user else "User"
        self.hello_name = QLabel(name + "!")
        self.hello_name.setFont(QFont("Helvetica Neue", 26, QFont.Bold))
        self.hello_name.setStyleSheet(f"color: {ORANGE}; background: transparent;")
        hello_row.addWidget(hello_prefix)
        hello_row.addWidget(self.hello_name)
        hello_row.addStretch()
        layout.addLayout(hello_row)

        layout.addSpacing(16)

        # ── Progress Card ────────────────────────────────────────────────────
        self.progress_card = ProgressCard()
        layout.addWidget(self.progress_card)

        layout.addSpacing(16)

        # ── Today Habit ──────────────────────────────────────────────────────
        habits_header = SectionHeader("Today Habit", "See all", bg=BG)
        layout.addWidget(habits_header)

        layout.addSpacing(6)

        self.habits_card = HabitsCard(HABITS)
        layout.addWidget(self.habits_card)

        layout.addSpacing(20)

        # ── Your Goals ───────────────────────────────────────────────────────
        goals_header = SectionHeader("Your Goals", "See all", bg=BG)
        layout.addWidget(goals_header)

        layout.addSpacing(6)

        for g in GOALS:
            gc = GoalCard(g)
            layout.addWidget(gc)
            layout.addSpacing(8)

        # Spacer at bottom for FAB clearance
        layout.addSpacing(80)
        layout.addStretch()

    def set_user(self, session: dict):
        self.user = session
        self._build_page()

        # update habits/goals (optional future improvement)

    def _open_modal(self):
        self.modal = NewHabitModal(self, on_save=self._on_modal_save)

    def _on_modal_save(self):
        # Rebuild page content
        self._build_page()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'modal') and self.modal.isVisible():
            self.modal.setGeometry(0, 0, self.width(), self.height())
        self._reposition_fab()