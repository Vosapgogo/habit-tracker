from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Signal
from pages.components.form_input import FormInputField
from pages.constants import APP_FONT, BORDER, ORANGE, TEXT_D, TEXT_M, WHITE
from pages.utils.helpers import prevent_double_click

import models.user_session as user_session

from pages.components.primary_button import PrimaryButton

PERIOD = {
    "1 Week (7 Days)": 7,
    "2 Weeks (14 Days)": 14,
    "1 Month (30 Days)": 30,
    "3 Months (90 Days)": 90,
}


class NewHabitModal(QWidget):
    habit_submitted = Signal(str, str, int, str)
    habit_updated = Signal(str, str, str, int, str)

    def __init__(self, parent, habit=None):
        super().__init__(parent)
        self._habit = habit
        self._is_edit = habit is not None

        self.setGeometry(0, 0, parent.width(), parent.height())
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background: rgba(245, 245, 245, 200);")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Modal card
        self.card = QFrame(self)
        self.card.setFixedWidth(340)
        self.card.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border-radius: 14px;
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(4, 4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(0)

        # Title row
        title_text = "Edit Habit Goal" if self._is_edit else "Create Habit Goal"

        title_row = QHBoxLayout()
        title_lbl = QLabel(title_text)
        title_lbl.setFont(QFont(APP_FONT, 16, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT_D}; margin-bottom: 5px;")
        title_lbl.setWordWrap(True)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet(
            f"background: transparent; color: {TEXT_M}; font-size: 18px; border: none;"
        )
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)

        title_row.addWidget(title_lbl)
        title_row.addStretch()
        title_row.addWidget(close_btn)
        layout.addLayout(title_row)

        layout.addSpacing(8)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet(f"background: {BORDER}; border: none; max-height: 1px;")
        layout.addWidget(div)
        layout.addSpacing(12)

        self.goal_entry = FormInputField("Your Goal")
        layout.addWidget(self.goal_entry)
        layout.addSpacing(12)

        self.name_entry = FormInputField("Habit Name")
        layout.addWidget(self.name_entry)
        layout.addSpacing(12)

        # Period dropdown
        period_lbl = QLabel("Period")
        period_lbl.setFont(QFont(APP_FONT, 12))
        period_lbl.setStyleSheet(f"color: {TEXT_M};")
        layout.addWidget(period_lbl)

        layout.addSpacing(4)

        self.period_combo = QComboBox()
        self.period_combo.addItems(
            [
                "1 Week (7 Days)",
                "2 Weeks (14 Days)",
                "1 Month (30 Days)",
                "3 Months (90 Days)",
            ]
        )
        self.period_combo.setCurrentIndex(2)
        self._style_combo(self.period_combo)
        layout.addWidget(self.period_combo)
        layout.addSpacing(12)

        # Type dropdown
        type_lbl = QLabel("Habit Type")
        type_lbl.setFont(QFont(APP_FONT, 12))
        type_lbl.setStyleSheet(f"color: {TEXT_M};")
        layout.addWidget(type_lbl)

        layout.addSpacing(4)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Everyday", "Weekdays", "Weekends"])
        self._style_combo(self.type_combo)
        layout.addWidget(self.type_combo)
        layout.addSpacing(16)

        # Create button
        btn_text = "Update" if self._is_edit else "Create New"
        create_btn = PrimaryButton(btn_text)
        create_btn.clicked.connect(self._save)
        layout.addWidget(create_btn)

        main_layout.addWidget(self.card)

        if self._is_edit:
            goal_data = self._get_goal_data()

            self.goal_entry.entry.setText(goal_data.get("goal", ""))
            self.name_entry.entry.setText(self._habit.get("name", ""))

            h_type = goal_data.get("type", "Everyday")
            self.type_combo.setCurrentText(h_type)

            days = goal_data.get("total_days", 30)
            for text, val in PERIOD.items():
                if val == days:
                    self.period_combo.setCurrentText(text)
                    break

        self.raise_()
        self.show()

    def _style_combo(self, combo):
        combo.setMinimumHeight(46)
        combo.setFont(QFont(APP_FONT, 13))
        combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {BORDER};
                border-radius: 10px;
                padding: 4px 10px;
                color: {TEXT_D};
                background: {WHITE};
            }}
            QComboBox:focus {{
                border: 1.5px solid {ORANGE};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
        """)

    def _get_goal_data(self):
        session = user_session.load_session()
        if not session:
            return {}

        habit_id = self._habit.get("id")

        for goal in session.get("goals", []):
            if goal.get("habit_id") == habit_id:
                return goal
        return {}

    @prevent_double_click(delay=1.5)
    def _save(self):
        goal_text = self.goal_entry.text().strip()
        name_text = self.name_entry.text().strip()

        if not goal_text or not name_text:
            return

        period_days = PERIOD[self.period_combo.currentText()]
        habit_type = self.type_combo.currentText()

        if self._is_edit:
            self.habit_updated.emit(
                self._habit["id"], goal_text, name_text, period_days, habit_type
            )
        else:
            self.habit_submitted.emit(goal_text, name_text, period_days, habit_type)

        self.close()

    def mousePressEvent(self, event):
        if not self.card.geometry().contains(event.position().toPoint()):
            self.close()
