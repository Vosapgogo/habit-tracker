from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.constants import *
from pages.utils.helpers import * 

class GoalCard(QWidget):
    def __init__(self, goal, parent=None):
        super().__init__(parent)
        self.goal = goal
        self.setFixedHeight(95)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        card_rect = QRect(0, 0, self.width(), 90)
        path = rounded_rect_path(card_rect, 14)
        p.fillPath(path, QColor(WHITE))

        g = self.goal

        # Goal name
        f_body = QFont("Helvetica Neue", 13)
        p.setFont(f_body)
        p.setPen(QColor(TEXT_D))
        p.drawText(QRect(16, 10, self.width() - 60, 28), Qt.AlignLeft | Qt.AlignVCenter, g["name"])

        # Three dots
        p.setPen(QColor(TEXT_L))
        f_dots = QFont("Helvetica Neue", 18)
        p.setFont(f_dots)
        p.drawText(QRect(self.width() - 36, 6, 30, 28), Qt.AlignCenter, "⋮")

        # Progress bar background
        bar_x0, bar_y0 = 16, 42
        bar_w = self.width() - 100
        bar_h = 10
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#F0F0F0"))
        p.drawRoundedRect(bar_x0, bar_y0, bar_w, bar_h, 5, 5)

        # Progress bar fill
        fill_w = int(bar_w * g["progress"])
        p.setBrush(QColor(ORANGE))
        p.drawRoundedRect(bar_x0, bar_y0, fill_w, bar_h, 5, 5)

        # Target text
        f_xs = QFont("Helvetica Neue", 10)
        p.setFont(f_xs)
        p.setPen(QColor(TEXT_L))
        p.drawText(QRect(16, 56, 220, 16), Qt.AlignLeft | Qt.AlignVCenter, g["target"])

        # Type text (orange)
        p.setPen(QColor(ORANGE))
        p.drawText(QRect(16, 68, 220, 16), Qt.AlignLeft | Qt.AlignVCenter, g["type"])

        p.end()
