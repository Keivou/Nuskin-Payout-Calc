import sys
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, 
QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox)
from PySide6.QtCore import Slot

class AddProductForm(QDialog):
    def __init__(self, parent=None):
        super(AddProductForm, self).__init__(parent)
        self.setWindowTitle("Add Product Tab")