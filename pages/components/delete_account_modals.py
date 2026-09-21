import os
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QFont, QColor, QMouseEvent, QPixmap
from PySide6.QtCore import Qt, Signal
from pages.constants import APP_FONT, WHITE, TEXT_D, TEXT_M, ORANGE, ORANGE_L, BORDER
from pages.components.primary_button import PrimaryButton
from pages.utils.helpers import prevent_double_click

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path_bin = os.path.join(BASE_DIR, "images", "trash_bin.png")
img_path_success = os.path.join(BASE_DIR, "images", "bin_success.png")


class DeleteAccountConfirmModal(QWidget):
    confirm_delete = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        self.setGeometry(0, 0, parent.width(), parent.height())
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background: rgba(200, 200, 200, 180);")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        self.card = QFrame(self)
        self.card.setFixedWidth(320)
        self.card.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border-radius: 14px;
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(20, 16, 20, 24)
        layout.setSpacing(0)

        # Close button
        close_row = QHBoxLayout()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet(
            f"background: transparent; color: {TEXT_M}; font-size: 18px; border: none;"
        )
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        close_row.addStretch()
        close_row.addWidget(close_btn)
        layout.addLayout(close_row)
        layout.addSpacing(8)

        # Divider line
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet(f"background: {BORDER}; border: none; max-height: 1px;")
        layout.addWidget(div)
        layout.addSpacing(16)

        # Icon and title
        icon_lbl = QLabel()
        pixmap = QPixmap(img_path_bin)
        scaled = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_lbl.setPixmap(scaled)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("background: transparent;")
        layout.addWidget(icon_lbl)

        layout.addSpacing(16)

        title_lbl = QLabel("Are you sure want to delete account?")
        title_lbl.setFont(QFont(APP_FONT, 14, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        layout.addSpacing(20)

        # Delete and Cancel buttons
        del_btn = PrimaryButton("Delete")
        del_btn.clicked.connect(self._on_delete_clicked)
        layout.addWidget(del_btn)

        layout.addSpacing(12)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(30)
        cancel_btn.setFont(QFont(APP_FONT, 13, QFont.Bold))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_D};
                border: none;
            }}
            QPushButton:hover {{ color: {TEXT_M}; }}
        """)
        cancel_btn.clicked.connect(self.close)
        layout.addWidget(cancel_btn)

        main_layout.addWidget(self.card)

        self.raise_()
        self.show()

    @prevent_double_click(delay=1.5)
    def _on_delete_clicked(self):
        self.confirm_delete.emit()
        self.close()

    def mousePressEvent(self, event: QMouseEvent):
        if not self.card.geometry().contains(event.position().toPoint()):
            self.close()


class DeleteAccountSuccessModal(QWidget):
    success_ok = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        self.setGeometry(0, 0, parent.width(), parent.height())
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background: rgba(200, 200, 200, 180);")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        self.card = QFrame(self)
        self.card.setFixedWidth(320)
        self.card.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border-radius: 16px;
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(20, 16, 20, 24)
        layout.setSpacing(0)

        # Close button
        close_row = QHBoxLayout()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet(
            f"background: transparent; color: {TEXT_M}; font-size: 18px; border: none;"
        )
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self._on_ok_clicked)

        close_row.addStretch()
        close_row.addWidget(close_btn)
        layout.addLayout(close_row)
        layout.addSpacing(8)

        # Divider line
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet(f"background: {BORDER}; border: none; max-height: 1px;")
        layout.addWidget(div)
        layout.addSpacing(8)

        # Icon and Title
        icon_lbl = QLabel()
        pixmap = QPixmap(img_path_success)
        scaled = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_lbl.setPixmap(scaled)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("background: transparent;")
        layout.addWidget(icon_lbl)

        layout.addSpacing(16)

        title_lbl = QLabel("You successfuly deleted account")
        title_lbl.setFont(QFont(APP_FONT, 14, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT_D}; background: transparent;")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        layout.addSpacing(24)

        # Ok button
        ok_btn = QPushButton("Ok")
        ok_btn.setFixedHeight(46)
        ok_btn.setFont(QFont(APP_FONT, 14, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ORANGE}, stop:1 {ORANGE_L});
                color: {WHITE};
                border-radius: 12px;
                border: none;
            }}
            QPushButton:hover {{ background: {ORANGE_L}; }}
            QPushButton:pressed {{ background: #E05010; }}
        """)
        ok_btn.clicked.connect(self._on_ok_clicked)
        layout.addWidget(ok_btn)

        main_layout.addWidget(self.card)

        self.raise_()
        self.show()

    def _on_ok_clicked(self):
        self.success_ok.emit()
        self.close()

    def mousePressEvent(self, event: QMouseEvent):
        if not self.card.geometry().contains(event.position().toPoint()):
            self._on_ok_clicked()
