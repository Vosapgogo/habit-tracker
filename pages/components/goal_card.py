from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QWidget,
    QPushButton,
    QFrame,
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtCore import Qt, QPoint, QRect, Signal
from pages.constants import APP_FONT, BG, BORDER, ORANGE, TEXT_D, TEXT_L, WHITE
from pages.utils.helpers import rounded_rect_path


class GoalCard(QWidget):
    edit_requested = Signal(dict)
    delete_requested = Signal(dict)

    def __init__(self, goal, parent=None):
        super().__init__(parent)
        self.goal = goal
        self.setFixedHeight(95)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._popup = None

    def mousePressEvent(self, event):
        click_zone = QRect(self.width() - 40, 0, 40, 40)

        if click_zone.contains(event.position().toPoint()):
            self._show_popup(event.globalPosition().toPoint())

    def _show_popup(self, global_pos):
        if self._popup:
            self._popup.close()

        self._popup = QFrame()
        self._popup.setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self._popup.setAttribute(Qt.WA_TranslucentBackground)

        self._popup.setMinimumWidth(110)

        container = QFrame(self._popup)
        container.setGeometry(0, 0, 110, 56)
        container.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border-radius: 12px;
                border: 1px solid {BORDER};
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)
        shadow.setOffset(2, 4)
        shadow.setColor(QColor(0, 0, 0, 50))
        self._popup.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self._popup)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(0)

        def make_btn(text, color, on_click):
            btn = QPushButton(text)
            btn.setMinimumHeight(24)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {color};
                    border: none;
                    text-align: left;
                    padding-left: 14px;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background: {BG};
                }}
            """)
            btn.clicked.connect(on_click)
            return btn

        layout.addWidget(make_btn("Edit", TEXT_D, self._on_edit))
        layout.addWidget(make_btn("Delete", ORANGE, self._on_delete))

        local_pos = QPoint(self.width() - 115, 0)
        global_pos = self.mapToGlobal(local_pos)

        self._popup.move(global_pos)
        self._popup.show()

    def _on_edit(self):
        self._popup.close()
        self.edit_requested.emit(self.goal)

    def _on_delete(self):
        self._popup.close()
        self.delete_requested.emit(self.goal)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        card_rect = QRect(0, 0, self.width(), 90)
        path = rounded_rect_path(card_rect, 14)
        p.fillPath(path, QColor("#F8F8F8"))

        g = self.goal

        # Goal name
        f_body = QFont(APP_FONT, 13)
        p.setFont(f_body)
        p.setPen(QColor(TEXT_D))

        metrics = p.fontMetrics()
        max_text_width = self.width() - 60
        elided_name = metrics.elidedText(g["name"], Qt.ElideRight, max_text_width)

        p.drawText(
            QRect(16, 10, max_text_width, 28),
            Qt.AlignLeft | Qt.AlignVCenter,
            elided_name,
        )

        # Three dots
        p.setPen(QColor(TEXT_L))
        f_dots = QFont(APP_FONT, 18)
        p.setFont(f_dots)
        p.drawText(QRect(self.width() - 36, 6, 30, 28), Qt.AlignCenter, "⋮")

        # Progress bar background
        bar_x0, bar_y0 = 16, 42
        bar_w = self.width() - 100
        bar_h = 10
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#F0F0F0"))
        p.drawRoundedRect(bar_x0, bar_y0, bar_w, bar_h, 2, 2)

        # Progress bar fill
        fill_w = int(bar_w * g["progress"])
        p.setBrush(QColor(ORANGE))
        p.drawRoundedRect(bar_x0, bar_y0, fill_w, bar_h, 2, 2)

        # Target text
        f_xs = QFont(APP_FONT, 10)
        p.setFont(f_xs)
        p.setPen(QColor(TEXT_L))
        p.drawText(QRect(16, 56, 220, 16), Qt.AlignLeft | Qt.AlignVCenter, g["target"])

        # Type text
        p.setPen(QColor(ORANGE))
        p.drawText(QRect(16, 68, 220, 16), Qt.AlignLeft | Qt.AlignVCenter, g["type"])

        p.end()
