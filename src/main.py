import sys
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, 
QLabel, QLineEdit, QVBoxLayout)
from PySide6.QtCore import Slot

from widgets.main_widget import MainWidget
from windows.main_window import MainWindow


def main():
    # QtApp
    app = QApplication(sys.argv)

    widget = MainWidget()

    window = MainWindow(widget)
    # window.resize(800, 600)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()