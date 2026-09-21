import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from pages.app import App
from pages.constants import APP_FONT

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    app.setFont(QFont(APP_FONT, 11))  

    window = App()                
    window.show()
    sys.exit(app.exec())