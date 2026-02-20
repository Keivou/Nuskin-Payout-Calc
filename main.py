import sys
import sqlite3
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, 
QLabel, QLineEdit, QVBoxLayout)
from PySide6.QtCore import Slot

from src.widgets.main_widget import MainWidget
from src.windows.main_window import MainWindow

from src.init.init_tables import *

from qt_material import apply_stylesheet


def main(connection=None):
    # Initialize product table if products.db doesn't exist
    if connection:
        init_product_table(connection)

    # QtApp
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")

    # Create MainWidget
    widget = MainWidget()

    # Create MainWindow
    window = MainWindow(widget)
    window.show()

    # Execute App
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        # Connect to SQLite Database and create a cursor
        connection = sqlite3.connect("./src/databases/products.db")
        main(connection)

    except sqlite3.Error as error:
        print("Error occurred -", error)
        main()
    
    