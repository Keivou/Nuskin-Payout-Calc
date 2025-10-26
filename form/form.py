import sys
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, 
QLabel, QLineEdit, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Slot

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Nu Skin Payout Calculator")

        # Overall vertical layout
        vertical_layout = QVBoxLayout(self)

        # Horizontal layouts to stack
        marketbox = self.market()
        productbox = self.product()
        dcsvbox = self.dc_sv_payout()
        pracsvbox = self.prac_sv_payout()
        gsvbox = self.gsv_payout()
        ltsvbox = self.ltsv_payout()

        # Stacking the layouts
        vertical_layout.addLayout(marketbox)
        vertical_layout.addLayout(productbox)
        vertical_layout.addLayout(dcsvbox)
        vertical_layout.addLayout(pracsvbox)
        vertical_layout.addLayout(gsvbox)
        vertical_layout.addLayout(ltsvbox)

        # Adding button
        self.calc_button = self.calculate_total_payout()
        vertical_layout.addWidget(self.calc_button)

        # Setting the layout for the window
        self.setLayout(vertical_layout)

        # Button doesn't exist yet
        self.calc_button.clicked.connect(self.calculate_total_payout)

    def market(self):
        hbox = QHBoxLayout()

        # Market widgets
        self.market_label = QLabel("Mercado:")
        self.market_location = QLineEdit("")

        # Add widgets to horizontal box
        hbox.addWidget(self.market_label)
        hbox.addWidget(self.market_location)
        
        return hbox

    def product(self):
        hbox = QHBoxLayout()

        # Product widgets
        self.product_label = QLabel("Producto:")
        self.product_name = QLineEdit("")

        # Quantity widgets
        self.quantity_label = QLabel("Cantidad:")
        self.quantity_value = QLineEdit("")

        # Add widgets to horizontal box
        hbox.addWidget(self.product_label)
        hbox.addWidget(self.product_name)
        hbox.addWidget(self.quantity_label)
        hbox.addWidget(self.quantity_value)

        return hbox

    def dc_sv_payout(self):
        hbox = QHBoxLayout()

        # DC-SV widgets
        self.dcsv_label = QLabel("DC-SV:")
        self.dcsv_value = QLineEdit("")

        hbox.addWidget(self.dcsv_label)
        hbox.addWidget(self.dcsv_value)

        return hbox

    def prac_sv_payout(self):
        hbox = QHBoxLayout()

        # PRAC-SV widgets
        self.pracsv_label = QLabel("PRAC-SV:")
        self.pracsv_value = QLineEdit("")

        hbox.addWidget(self.pracsv_label)
        hbox.addWidget(self.pracsv_value)

        return hbox

    def gsv_payout(self):
        hbox = QHBoxLayout()

        # GSV widgets
        self.gsv_label = QLabel("GSV/VVG:")
        self.gsv_value = QLineEdit("")

        hbox.addWidget(self.gsv_label)
        hbox.addWidget(self.gsv_value)

        return hbox

    def ltsv_payout(self):
        hbox = QHBoxLayout()

        # LTSV widgets
        self.ltsv_label = QLabel("LTSV:")
        self.ltsv_value = QLineEdit("")

        hbox.addWidget(self.ltsv_label)
        hbox.addWidget(self.ltsv_value)

        return hbox

    def calculate_total_payout(self):
        button = QPushButton("Calc Payout")
        try:
            dcsv = float(self.dcsv_value.text())
            pracsv = float(self.pracsv_value.text())
            gsv = float(self.gsv_value.text())
            ltsv = float(self.ltsv_value.text())
        except ValueError:
            # This is only triggered when the app starts
            return button

        payout = dcsv + pracsv + gsv + ltsv
        print(payout)
        return button