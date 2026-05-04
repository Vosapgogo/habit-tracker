import sys
from PySide6.QtWidgets import QApplication
from pages.app import App

if __name__ == "__main__":
    app = QApplication(sys.argv)  # ← завжди створюємо першим
    window = App()                # ← App сам перевіряє сесію в _startup()
    window.show()
    sys.exit(app.exec())