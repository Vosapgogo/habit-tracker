from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.constants import *
from pages.utils.helpers import * 

class HabitsCard(QWidget):
    def __init__(self, habits, parent=None):
        super().__init__(parent)
        self.habits = habits
        h = len(habits) * 60 + 16
        self.setFixedHeight(h)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Card background
        path = rounded_rect_path(self.rect(), 16)
        p.fillPath(path, QColor(WHITE))

        for i, h in enumerate(self.habits):
            y = 8 + i * 60

            # Green highlight if done
            if h["done"]:
                hl_path = QPainterPath()
                hl_path.addRoundedRect(14, y, self.width() - 28, 44, 10, 10)
                p.fillPath(hl_path, QColor(GREEN_L))

            # Name text
            f_body = QFont("Helvetica Neue", 13)
            p.setFont(f_body)
            p.setPen(QColor(GREEN if h["done"] else TEXT_D))
            p.drawText(QRect(24, y, 260, 44), Qt.AlignLeft | Qt.AlignVCenter, h["name"])

            # Checkbox
            box_rect = QRect(self.width() - 72, y + 10, 26, 26)
            if h["done"]:
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(GREEN))
                p.drawRoundedRect(box_rect, 6, 6)  # 6 — радіус кутів
                p.setPen(QColor(WHITE))
                f_check = QFont("Helvetica Neue", 12, QFont.Bold)
                p.setFont(f_check)
                p.drawText(box_rect, Qt.AlignCenter, "✓")
            else:
                p.setPen(QPen(QColor(BORDER), 2))
                p.setBrush(QColor(WHITE))
                p.drawRoundedRect(box_rect, 6, 6)

            # Three dots
            p.setPen(QColor(TEXT_L))
            f_dots = QFont("Helvetica Neue", 18)
            p.setFont(f_dots)
            p.drawText(QRect(self.width() -46, y, 30, 44), Qt.AlignCenter, "⋮")

            # Divider
            if i < len(self.habits) - 1:
                p.setPen(QPen(QColor(BORDER), 1))
                p.drawLine(14, y + 52, self.width() - 14, y + 52)

        p.end()