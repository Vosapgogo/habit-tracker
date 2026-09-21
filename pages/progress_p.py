import datetime
from dateutil.relativedelta import relativedelta

from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal

from pages.components.bottom_nav import BottomNav
from pages.components.donut_cart import DonutChart
from pages.components.goal_progress_card import GoalProgressItem

from pages.constants import APP_FONT, BG, ORANGE, TEXT_D, TEXT_M, WHITE


class ProgressPage(QMainWindow):
    go_home = Signal()
    see_all_goals = Signal(list)
    nav_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress")
        self.setFixedSize(390, 780)
        self.user = None

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet(f"background: {BG};")

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{ background: {BG}; border: none; }}
            QScrollBar:vertical {{ width: 0px; background: transparent; }}
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet(f"background: {BG};")
        self.scroll.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll)

        self.nav = BottomNav(active_tab="Activity")
        self.nav.tab_requested.connect(self._on_nav_clicked)
        main_layout.addWidget(self.nav)

        self._build_page()

    def set_user(self, session: dict):
        self.user = session
        self._on_filter_changed(self.combo.currentText())

    def _on_nav_clicked(self, tab_name):
        self.nav_requested.emit(tab_name)

    def _build_page(self):
        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(16, 26, 16, 16)
        layout.setSpacing(0)

        title = QLabel("Progress")
        title.setFont(QFont(APP_FONT, 28, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_D};")
        layout.addWidget(title)

        layout.addSpacing(16)

        sub_row = QHBoxLayout()
        sub_title = QLabel("Progress Report")
        sub_title.setFont(QFont(APP_FONT, 20, QFont.Bold))
        sub_title.setStyleSheet(f"color: {TEXT_D};")

        self.combo = QComboBox()
        self.combo.addItems(
            ["This Week", "2 Weeks", "This Month", "3 Months", "This Year"]
        )
        self.combo.setFixedHeight(34)
        self.combo.setFont(QFont(APP_FONT, 13))
        self.combo.setStyleSheet(f"""
            QComboBox {{ background: #E8E8E8; color: {TEXT_D}; border-radius: 6px; padding: 4px 10px; }}
            QComboBox::drop-down {{ border: none; width: 26px; }}
        """)
        self.combo.currentTextChanged.connect(self._on_filter_changed)

        sub_row.addWidget(sub_title)
        sub_row.addStretch()
        sub_row.addWidget(self.combo)
        layout.addLayout(sub_row)
        layout.addSpacing(24)

        self.card_layout_container = QVBoxLayout()
        self.card_layout_container.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.card_layout_container)
        layout.addStretch()

    def _on_filter_changed(self, filter_text):
        if not self.user:
            return
        today = datetime.date.today()

        match filter_text:
            case "This Week":
                start_date = today - datetime.timedelta(days=today.weekday())
            case "2 Weeks":
                start_date = today - datetime.timedelta(days=14)
            case "This Month":
                start_date = today.replace(day=1)
            case "3 Months":
                start_date = today - relativedelta(months=3)
            case "This Year":
                start_date = today.replace(month=1, day=1)
            case _:
                start_date = today.replace(year=2000)

        goals = [
            g
            for g in self.user.get("goals", [])
            if datetime.datetime.strptime(
                g.get("created_date", "2000-01-01"), "%Y-%m-%d"
            ).date()
            >= start_date
        ]

        self._build_card(goals)

    def _build_card(self, filtered_goals):
        layout = self.card_layout_container.layout()
        if layout:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        card = QWidget()
        card.setStyleSheet(f"QWidget {{ background: {WHITE}; border-radius: 16px; }}")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 20, 16, 20)

        # Header
        header = QHBoxLayout()
        title = QLabel("Your Goals")
        title.setFont(QFont(APP_FONT, 16, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_D};")

        see_all = QPushButton("See All")
        see_all.setStyleSheet(
            f"color: {ORANGE}; background: transparent; border: none;"
        )
        see_all.setCursor(Qt.PointingHandCursor)
        all_user_goals = self.user.get("goals", [])
        see_all.clicked.connect(lambda: self.see_all_goals.emit(all_user_goals))

        header.addWidget(title)
        header.addStretch()
        header.addWidget(see_all)
        card_layout.addLayout(header)

        card_layout.addSpacing(24)

        # filtered_goals
        total = len(filtered_goals)
        achieved = sum(1 for g in filtered_goals if g.get("done"))
        unachieved = total - achieved
        pct = (achieved / total * 100) if total > 0 else 0

        chart_row = QHBoxLayout()
        chart_row.addWidget(DonutChart(percentage=pct), alignment=Qt.AlignCenter)
        card_layout.addLayout(chart_row)

        card_layout.addSpacing(24)

        def make_status(icon, text, color):
            lbl = QLabel(f"{icon} {text}")
            lbl.setFont(QFont(APP_FONT, 12, QFont.Bold))
            lbl.setStyleSheet(f"color: {color};")
            lbl.setAlignment(Qt.AlignCenter)
            return lbl

        card_layout.addWidget(
            make_status("✓", f"{achieved} Habits goal has achieved", ORANGE),
            alignment=Qt.AlignCenter,
        )
        card_layout.addWidget(
            make_status("×", f"{unachieved} Habits goal hasn't achieved", TEXT_M),
            alignment=Qt.AlignCenter,
        )

        card_layout.addSpacing(10)

        if total == 0:
            empty_lbl = QLabel("No goals found for this period")
            empty_lbl.setStyleSheet(f"color: {TEXT_M};")
            card_layout.addWidget(empty_lbl, alignment=Qt.AlignCenter)
        else:
            for g in filtered_goals[:3]:
                card_layout.addWidget(GoalProgressItem(g))
                card_layout.addSpacing(8)

            bottom_see_all = QPushButton("See All")
            bottom_see_all.setStyleSheet(
                f"color: {ORANGE}; background: transparent; border: none;"
            )
            bottom_see_all.setCursor(Qt.PointingHandCursor)
            bottom_see_all.clicked.connect(
                lambda: self.see_all_goals.emit(filtered_goals)
            )
            card_layout.addWidget(bottom_see_all)

        self.card_layout_container.addWidget(card)
        self.card_layout_container.addStretch()
