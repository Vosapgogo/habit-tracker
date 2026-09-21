from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
from pages.constants import APP_FONT, BG, ORANGE, TEXT_D, TEXT_M, WHITE
from pages.components.goal_progress_card import GoalProgressItem


class GoalsPage(QWidget):
    go_home = Signal()
    go_progress = Signal()

    update_habit_requested = Signal(str, str, str, int, str)
    delete_habit_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background: {BG};")
        self._goals = []
        self._filter = "All"

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { width: 0px; background: transparent; }
        """)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        root = QVBoxLayout(content)
        root.setContentsMargins(16, 20, 16, 16)
        root.setSpacing(0)

        # Header
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
        back_btn.clicked.connect(self.go_back_to_progress)

        title_lbl = QLabel("Your Goals")
        title_lbl.setFont(QFont(APP_FONT, 20, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT_D}; background: transparent;")

        header.addWidget(back_btn)
        header.addSpacing(8)
        header.addWidget(title_lbl)
        header.addStretch()

        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Achieved", "Unachieved"])
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

        root.addLayout(header)
        root.addSpacing(20)

        self.container = QWidget()
        self.container.setStyleSheet(f"""
            QWidget {{
                background: {WHITE};
                border-radius: 16px;
            }}
        """)

        self._list_layout = QVBoxLayout(self.container)
        self._list_layout.setContentsMargins(12, 12, 12, 12)
        self._list_layout.setSpacing(10)

        root.addWidget(self.container)

        root.addStretch()

    def set_specific_goals(self, goals):
        self._goals = goals
        self._build_page()

    def set_user(self, session):
        self._goals = session.get("goals", [])
        self._build_page()

    def _apply_filter(self, option):
        self._filter = option
        self._build_page()

    def _build_page(self):
        while self._list_layout.count() > 0:
            item = self._list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.spacerItem():
                self._list_layout.removeItem(item)

        goals = self._goals
        if self._filter == "Achieved":
            goals = [g for g in goals if g.get("done")]
        elif self._filter == "Unachieved":
            goals = [g for g in goals if not g.get("done")]

        if not goals:
            empty = QLabel("No goals here yet")
            empty.setAlignment(Qt.AlignCenter)
            empty.setFont(QFont(APP_FONT, 14))
            empty.setStyleSheet(f"color: {TEXT_M}; background: transparent;")

            self._list_layout.addSpacing(20)
            self._list_layout.addWidget(empty)
            self._list_layout.addSpacing(20)
            return

        for goal in goals:
            card = GoalProgressItem(goal)
            self._list_layout.addWidget(card)

    def go_back_to_progress(self):
        self.go_progress.emit()
