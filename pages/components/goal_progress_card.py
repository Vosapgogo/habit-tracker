from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from pages.constants import APP_FONT, TEXT_D, TEXT_M


class GoalProgressItem(QFrame):
    def __init__(self, goal, parent=None):
        super().__init__(parent)
        self.setFixedHeight(64)
        self.setStyleSheet(f"background: #F8F8F8; border-radius: 12px;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        progress = int(goal.get("progress", 0) * 100)
        is_done = goal.get("done", False)
        color = "#4CAF50" if progress == 100 else TEXT_M

        pct_lbl = QLabel(f"{progress}%")
        pct_lbl.setFixedSize(40, 40)
        pct_lbl.setAlignment(Qt.AlignCenter)
        pct_lbl.setFont(QFont(APP_FONT, 10, QFont.Bold))
        pct_lbl.setStyleSheet(f"""
            QLabel {{
                color: {color};
                border: 2px solid {color};
                border-radius: 20px;
                background: transparent;
            }}
        """)
        layout.addWidget(pct_lbl)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        text_col.setAlignment(Qt.AlignVCenter)

        title = QLabel(goal.get("habit_name", "Habit"))
        title.setFont(QFont(APP_FONT, 13, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        title.setWordWrap(True)

        sub = QLabel(
            f"{goal.get('done_count', 0)} from {goal.get('total_days', 1)} days target"
        )
        sub.setFont(QFont(APP_FONT, 11))
        sub.setStyleSheet(f"color: {TEXT_M}; background: transparent;")
        sub.setWordWrap(True)

        text_col.addWidget(title)
        text_col.addWidget(sub)
        layout.addLayout(text_col)

        layout.addStretch()

        badge = QLabel("Achieved" if is_done else "Unachieved")
        badge.setFont(QFont(APP_FONT, 13))
        badge.setAlignment(Qt.AlignCenter)
        badge.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        badge.setMinimumWidth(90)

        if is_done:
            badge.setStyleSheet(
                f"color: #4CAF50; background: #E8F5E9; border-radius: 12px; padding: 4px 8px;"
            )
        else:
            badge.setStyleSheet(
                f"color: {TEXT_M}; background: transparent; padding: 4px 8px;"
            )

        layout.addWidget(badge, 0, Qt.AlignRight | Qt.AlignVCenter)
