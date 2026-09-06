import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from app.constants import APP_TITLE, APP_VERSION
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    app.setApplicationVersion(APP_VERSION)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()