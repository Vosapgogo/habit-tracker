from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.constants import *
from pages.utils.helpers import * 

class ProgressCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Card background
        path = rounded_rect_path(self.rect(), 18)
        p.fillPath(path, QColor(ORANGE))

        # Ring parameters
        cx, cy, rad = 68, 60, 38
        pen_bg = QPen(QColor("#FF9966"), 8)
        pen_fg = QPen(QColor(WHITE), 8)
        pen_bg.setCapStyle(Qt.FlatCap)
        pen_fg.setCapStyle(Qt.RoundCap)

        rect_arc = QRect(cx - rad, cy - rad, rad * 2, rad * 2)

        # Background arc
        p.setPen(pen_bg)
        p.drawArc(rect_arc, 90 * 16, -360 * 16)

        # Progress arc (70%)
        p.setPen(pen_fg)
        p.drawArc(rect_arc, 90 * 16, -int(360 * 0.70) * 16)

        # Center text "70%"
        p.setPen(QColor(WHITE))
        f_pct = QFont("Helvetica Neue", 17, QFont.Bold)
        p.setFont(f_pct)
        p.drawText(QRect(cx - rad, cy - 14, rad * 2, 28), Qt.AlignCenter, "70%")

        # Right side text
        f_bold = QFont("Helvetica Neue", 15, QFont.Bold)
        p.setFont(f_bold)
        p.setPen(QColor(WHITE))
        p.drawText(QRect(140, 30, 200, 28), Qt.AlignLeft | Qt.AlignVCenter, "3 of 5 habits")

        f_small = QFont("Helvetica Neue", 11)
        p.setFont(f_small)
        p.setPen(QColor("#FFE0CC"))
        p.drawText(QRect(140, 58, 200, 24), Qt.AlignLeft | Qt.AlignVCenter, "completed today!")

        p.end()