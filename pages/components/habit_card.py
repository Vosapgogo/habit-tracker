from PySide6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QPushButton,
    QFrame,
    QVBoxLayout,
    QSizePolicy,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtCore import Qt, QPoint, QRect, Signal
from pages.constants import (
    APP_FONT,
    BG,
    BORDER,
    GREEN,
    GREEN_L,
    ORANGE,
    TEXT_D,
    TEXT_L,
    WHITE,
)
from pages.utils.helpers import rounded_rect_path
import models.user_session as user_session


class HabitCard(QWidget):
    habit_toggled = Signal()
    edit_requested = Signal(dict)
    delete_requested = Signal(dict)

    def __init__(self, habit, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.setFixedHeight(52)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._popup = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addStretch()

        self.check_btn = QPushButton(self)
        self.check_btn.setFixedSize(40, 52)
        self.check_btn.setCursor(Qt.PointingHandCursor)
        self.check_btn.setStyleSheet("background: transparent; border: none;")
        self.check_btn.clicked.connect(self._toggle)
        layout.addWidget(self.check_btn)

        self.dots_btn = QPushButton(self)
        self.dots_btn.setFixedSize(36, 52)
        self.dots_btn.setCursor(Qt.PointingHandCursor)
        self.dots_btn.setStyleSheet("background: transparent; border: none;")
        self.dots_btn.clicked.connect(self._handle_dots_click)
        layout.addWidget(self.dots_btn)

    def _handle_dots_click(self):
        global_pos = self.dots_btn.mapToGlobal(QPoint(0, self.height()))
        self._show_popup(global_pos)

    def _show_popup(self, global_pos):
        if self._popup:
            self._popup.close()

        self._popup = QFrame()
        self._popup.setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self._popup.setAttribute(Qt.WA_TranslucentBackground)
        self._popup.setFixedSize(110, 52)

        container = QFrame(self._popup)
        container.setGeometry(0, 0, 110, 52)
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

        self._popup.adjustSize()

        local_pos = QPoint(self.width() - self._popup.width() - 5, 0)
        global_pos = self.mapToGlobal(local_pos)
        self._popup.move(global_pos)

        self._popup.show()

    def _on_edit(self):
        self._popup.close()
        self.edit_requested.emit(self.habit)

    def _on_delete(self):
        self._popup.close()
        self.delete_requested.emit(self.habit)

    def _toggle(self):
        session = user_session.load_session()
        email = session.get("email") if session else None

        h = self.habit
        habit_id = h.get("id")
        done = h.get("done", False)

        if not email or not habit_id:
            return

        try:
            if done:
                user_session.mark_habit_undone(email, habit_id)
                h["done"] = False
            else:
                user_session.mark_habit_done(email, habit_id)
                h["done"] = True

        except user_session.UserNotFoundError as e:
            print(f"Error toggeling habit: {e}")
            return

        self.update()
        self.habit_toggled.emit()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        h = self.habit
        done = h["done"]

        bg_color = QColor(GREEN_L) if done else QColor("#F8F8F8")
        path = rounded_rect_path(QRect(0, 0, self.width(), self.height()), 12)
        p.fillPath(path, bg_color)

        # Name
        f = QFont(APP_FONT, 13)
        p.setFont(f)
        p.setPen(QColor(GREEN if done else TEXT_D))

        metrics = p.fontMetrics()
        max_text_width = self.width() - 90
        elided_name = metrics.elidedText(h["name"], Qt.ElideRight, max_text_width)

        p.drawText(
            QRect(14, 0, max_text_width, self.height()),
            Qt.AlignLeft | Qt.AlignVCenter,
            elided_name,
        )

        # Checkbox
        box = QRect(self.width() - 66, 13, 26, 26)
        if done:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(GREEN))
            p.drawRoundedRect(box, 6, 6)
            p.setPen(QColor(WHITE))
            p.setFont(QFont(APP_FONT, 12, QFont.Bold))
            p.drawText(box, Qt.AlignCenter, "✓")
        else:
            p.setPen(QPen(QColor(BORDER), 2))
            p.setBrush(QColor(WHITE))
            p.drawRoundedRect(box, 6, 6)

        # Three dots
        p.setPen(QColor(TEXT_L))
        p.setFont(QFont(APP_FONT, 18))
        p.drawText(QRect(self.width() - 36, 0, 30, self.height()), Qt.AlignCenter, "⋮")

        p.end()
