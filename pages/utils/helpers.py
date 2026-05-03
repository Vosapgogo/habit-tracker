from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.constants import *

def rounded_rect_path(rect: QRect, r: int = 12):
    path = QPainterPath()
    path.addRoundedRect(rect.x(), rect.y(), rect.width(), rect.height(), r, r)
    return path