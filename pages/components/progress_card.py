from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QFont, QColor, QPainter, QPen
from PySide6.QtCore import Qt, QRect
from pages.constants import APP_FONT, ORANGE, WHITE
from pages.utils.helpers import rounded_rect_path

import models.user_session as user_session


class ProgressCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habits = []
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_habits(self, habits: list):
        self.habits = habits
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        total = len(self.habits)
        done = sum(1 for h in self.habits if h.get("done"))
        pct = done / total if total > 0 else 0.0
        pct_text = f"{int(pct * 100)}%"
        label_text = f"{done} of {total} habits"

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

        # Background
        p.setPen(pen_bg)
        p.drawArc(rect_arc, 90 * 16, -360 * 16)

        # Progress
        p.setPen(pen_fg)
        p.drawArc(rect_arc, 90 * 16, -int(360 * pct) * 16)

        # Center text
        p.setPen(QColor(WHITE))
        f_pct = QFont(APP_FONT, 17, QFont.Bold)
        p.setFont(f_pct)
        p.drawText(QRect(cx - rad, cy - 14, rad * 2, 28), Qt.AlignCenter, pct_text)

        # Right side text
        f_bold = QFont(APP_FONT, 15, QFont.Bold)
        p.setFont(f_bold)
        p.setPen(QColor(WHITE))
        metrics_bold = p.fontMetrics()
        max_width = self.width() - 150
        elided_label = metrics_bold.elidedText(label_text, Qt.ElideRight, max_width)

        p.drawText(
            QRect(140, 30, max_width, 28), Qt.AlignLeft | Qt.AlignVCenter, elided_label
        )

        f_small = QFont(APP_FONT, 11)
        p.setFont(f_small)
        p.setPen(QColor("#FFE0CC"))
        p.drawText(
            QRect(140, 58, max_width, 24),
            Qt.AlignLeft | Qt.AlignVCenter,
            "completed today!",
        )

        p.end()
