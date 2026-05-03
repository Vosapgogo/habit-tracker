from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.constants import *
from pages.utils.helpers import * 

class NewHabitModal(QWidget):
    def __init__(self, parent, on_save):
        super().__init__(parent)
        self.on_save = on_save
        self.setGeometry(0, 0, parent.width(), parent.height())
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background: rgba(245, 245, 245, 200);")

        # Modal card
        self.card = QFrame(self)
        self.card.setGeometry(20, 160, 350, 390)
        self.card.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border-radius: 16px;
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
        title_row = QHBoxLayout()
        title_lbl = QLabel("Create New Habit Goal")
        title_lbl.setFont(QFont("Helvetica Neue", 15, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT_D};")
        close_btn = QLabel("×")
        close_btn.setFont(QFont("Helvetica Neue", 22))
        close_btn.setStyleSheet(f"color: {TEXT_M};")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.mousePressEvent = lambda e: self.close()
        title_row.addWidget(title_lbl)
        title_row.addStretch()
        title_row.addWidget(close_btn)
        layout.addLayout(title_row)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet(f"background: {BORDER}; border: none; max-height: 1px;")
        layout.addWidget(div)
        layout.addSpacing(8)

        def make_field(label_text):
            lbl = QLabel(label_text)
            lbl.setFont(QFont("Helvetica Neue", 11))
            lbl.setStyleSheet(f"color: {TEXT_M};")
            layout.addWidget(lbl)
            entry = QLineEdit()
            entry.setFont(QFont("Helvetica Neue", 13))
            entry.setFixedHeight(38)
            entry.setStyleSheet(f"""
                QLineEdit {{
                    border: 1px solid {BORDER};
                    border-radius: 8px;
                    padding: 4px 10px;
                    color: {TEXT_D};
                    background: {WHITE};
                }}
                QLineEdit:focus {{
                    border: 1.5px solid {ORANGE};
                }}
            """)
            layout.addWidget(entry)
            layout.addSpacing(4)
            return entry

        self.goal_entry = make_field("Your Goal")
        self.name_entry = make_field("Habit Name")

        # Period dropdown
        period_lbl = QLabel("Period")
        period_lbl.setFont(QFont("Helvetica Neue", 11))
        period_lbl.setStyleSheet(f"color: {TEXT_M};")
        layout.addWidget(period_lbl)
        self.period_combo = QComboBox()
        self.period_combo.addItems(["1 Week (7 Days)", "2 Weeks (14 Days)", "1 Month (30 Days)", "3 Months (90 Days)"])
        self.period_combo.setCurrentIndex(2)
        self._style_combo(self.period_combo)
        layout.addWidget(self.period_combo)
        layout.addSpacing(4)

        # Type dropdown
        type_lbl = QLabel("Habit Type")
        type_lbl.setFont(QFont("Helvetica Neue", 11))
        type_lbl.setStyleSheet(f"color: {TEXT_M};")
        layout.addWidget(type_lbl)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Everyday", "Weekdays", "Weekends", "Custom"])
        self._style_combo(self.type_combo)
        layout.addWidget(self.type_combo)
        layout.addSpacing(12)

        # Create button
        create_btn = QPushButton("Create New")
        create_btn.setFixedHeight(46)
        create_btn.setFont(QFont("Helvetica Neue", 14, QFont.Bold))
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ORANGE};
                color: {WHITE};
                border-radius: 23px;
                border: none;
            }}
            QPushButton:hover {{
                background: {ORANGE_L};
            }}
            QPushButton:pressed {{
                background: #E05010;
            }}
        """)
        create_btn.clicked.connect(self._save)
        layout.addWidget(create_btn)

        self.raise_()
        self.show()

    def _style_combo(self, combo):
        combo.setFixedHeight(38)
        combo.setFont(QFont("Helvetica Neue", 11))
        combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {BORDER};
                border-radius: 8px;
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

    def _save(self):
        goal_text = self.goal_entry.text().strip()
        name_text = self.name_entry.text().strip()
        if goal_text or name_text:
            GOALS.append({
                "name": goal_text or name_text,
                "progress": 0.0,
                "target": "0 from 7 days target",
                "type": self.type_combo.currentText()
            })
        self.on_save()
        self.close()

    def mousePressEvent(self, event):
        # Click outside card closes modal
        if not self.card.geometry().contains(event.position().toPoint()):
            self.close()

