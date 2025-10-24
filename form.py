import sys
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, 
QLabel, QLineEdit, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Slot

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Nu Skin Payout Calculator")

        # Add all widgets
        self.all_widgets()

        # Create layout and add widgets
        layout = QVBoxLayout(self)
        layout = self.design_layout(all_widgets)

        # Add button signal to greetings slot
        self.calculate_button.clicked.connect(self.greetings)

    
    def all_widgets(self):
        # Market widgets
        self.market_label = QLabel("Mercado:")
        self.market_dropdown = QLineEdit("")

        # Product widgets
        self.product_label = QLabel("Producto:")
        self.product_dropdown = QLineEdit("")

        # Quantity widgets
        self.quantity_label = QLabel("Cantidad:")
        self.quantity_value = QLineEdit("")

        # DC-SV widgets
        self.dcsv_label = QLabel("DC-SV:")
        self.dcsv_value = QLineEdit("")

        # PRAC-SV widgets
        self.pracsv_label = QLabel("PRAC-SV:")
        self.pracsv_value = QLineEdit("")

        # GSV widgets
        self.gsv_label = QLabel("GSV/VVG:")
        self.gsv_value = QLineEdit("")

        # LTSV widgets
        self.ltsv_label = QLabel("LTSV:")
        self.ltsv_value = QLineEdit("")

        # Calculate button widget
        self.calculate_button = QPushButton("Calc Payout")


    def market(self):
        hbox = QHBoxLayout()

        # Market widgets
        self.market_label = QLabel("Mercado:")
        self.market_location = QLineEdit("")

        # Add widgets to horizontal box
        hbox.addWidget(market_label)
        hbox.addWidget(market_location)
        
        return hbox

    def product():
        hbox = QHBoxLayout()

        # Product widgets
        self.product_label = QLabel("Producto:")
        self.product_name = QLineEdit("")

        # Quantity widgets
        self.quantity_label = QLabel("Cantidad:")
        self.quantity_value = QLineEdit("")

        # Add widgets to horizontal box
        hbox.addWidget(product_label)
        hbox.addWidget(product_name)
        hbox.addWidget(quantity_label)
        hbox.addWidget(quantity_value)

        return hbox

    def dc_sv_payout():
        hbox = QHBoxLayout()

        # DC-SV widgets
        self.dcsv_label = QLabel("DC-SV:")
        self.dcsv_value = QLineEdit("")

        hbox.addWidget(dcsv_label)
        hbox.addWidget(dcsv_value)

        return hbox

    def prac_sv_payout():
        hbox = QHBoxLayout()

        # PRAC-SV widgets
        self.pracsv_label = QLabel("PRAC-SV:")
        self.pracsv_value = QLineEdit("")

        hbox.addWidget(pracsv_label)
        hbox.addWidget(pracsv_value)

        return hbox

    def gsv_payout():
        hbox = QHBoxLayout()

        # GSV widgets
        self.gsv_label = QLabel("GSV/VVG:")
        self.gsv_value = QLineEdit("")

        hbox.addWidget(gsv_label)
        hbox.addWidget(gsv_value)

        return hbox

    def ltsv_payout():
        hbox = QHBoxLayout()

        # LTSV widgets
        self.ltsv_label = QLabel("LTSV:")
        self.ltsv_value = QLineEdit("")

        hbox.addWidget(ltsv_label)
        hbox.addWidget(ltsv_value)

        return hbox

    def calculate_total_payout():
        pass