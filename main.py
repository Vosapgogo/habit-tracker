import sys
from PySide6.QtWidgets import QApplication

from pages.home_p import App
from models.manager import load_data  

if __name__ == "__main__":
    data = load_data()

    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())