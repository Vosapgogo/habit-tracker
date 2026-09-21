from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QFont, QColor, QPainter, QPen
from PySide6.QtCore import Qt, QRect
from pages.constants import APP_FONT, ORANGE


class DonutChart(QWidget):
    def __init__(self, percentage, parent=None):
        super().__init__(parent)
        self.setFixedSize(140, 140)
        self.percentage = percentage

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = QRect(10, 10, 120, 120)
        pen_width = 16

        bg_pen = QPen(QColor("#F0F0F0"), pen_width)
        bg_pen.setCapStyle(Qt.FlatCap)
        p.setPen(bg_pen)
        p.drawArc(rect, 0, 360 * 16)

        if self.percentage > 0:
            fg_pen = QPen(QColor(ORANGE), pen_width)
            fg_pen.setCapStyle(Qt.FlatCap)
            p.setPen(fg_pen)
            span_angle = int(-(self.percentage / 100) * 360 * 16)
            p.drawArc(rect, 90 * 16, span_angle)

        p.setPen(QColor(ORANGE))
        p.setFont(QFont(APP_FONT, 22, QFont.Bold))
        p.drawText(rect, Qt.AlignCenter, f"{int(self.percentage)}%")
        p.end()
