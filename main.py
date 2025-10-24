import sys
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, 
QLabel, QLineEdit, QVBoxLayout)
from PySide6.QtCore import Slot

from form import Form


def main():
    # Create Application
    app = QApplication(sys.argv)

    # Create a form
    form = Form()
    form.show()

    # Exec App
    sys.exit(app.exec())


if __name__ == "__main__":
    main()