from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
QPushButton, QGroupBox, QTableView, QLineEdit, QComboBox)
from PySide6.QtCore import Qt, Slot, Signal

import sqlite3

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Overall vertical layout
        vertical_layout = QVBoxLayout(self)

        # Horizontal layouts to stack
        (marketbox, productbox, dcsvbox, pracsvbox, gsvbox, ltsvbox) = self.create_widgets()

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

    def create_menus(self):
        self._management_menu = self.menuBar().addMenu("&Gestionar")
        self._management_menu.addAction(self._add_product_action)
        self._management_menu.addAction(self._edit_product_action)

    def create_actions(self):
        self._add_product_action = QAction("Añadir Producto", self)
        self._edit_product_action = QAction("Editar Producto", self)
    
    def create_widgets(self):
        ## Market layout
        hbox = QHBoxLayout()

        # Market widgets
        self.market_widgets(hbox)

        ## Product layout
        hbox2 = QHBoxLayout()

        # Product widgets
        self.product_widgets(hbox2)

        # Quantity widgets
        self.quantity_label = QLabel("Cantidad:")
        self.quantity_value = QLineEdit("")

        # Add widgets to horizontal box
        hbox2.addWidget(self.quantity_label)
        hbox2.addWidget(self.quantity_value)

        ## DC-SV Layout
        hbox3 = QHBoxLayout()

        # DC-SV widgets
        self.dcsv_label = QLabel("DC-SV:")
        self.dcsv_value = QLineEdit("")

        # Add widgets to horizontal box
        hbox3.addWidget(self.dcsv_label)
        hbox3.addWidget(self.dcsv_value)

        ## PRAC-SV Layout
        hbox4 = QHBoxLayout()

        # PRAC-SV widgets
        self.pracsv_label = QLabel("PRAC-SV:")
        self.pracsv_value = QLineEdit("")

        # Add widgets to horizontal box
        hbox4.addWidget(self.pracsv_label)
        hbox4.addWidget(self.pracsv_value)

        ## GSV Layout
        hbox5 = QHBoxLayout()

        # GSV widgets
        self.gsv_label = QLabel("GSV/VVG:")
        self.gsv_value = QLineEdit("")

        # Add widgets to horizontal box
        hbox5.addWidget(self.gsv_label)
        hbox5.addWidget(self.gsv_value)

        ## LTSV Layout
        hbox6 = QHBoxLayout()

        # LTSV widgets
        self.ltsv_label = QLabel("LTSV:")
        self.ltsv_value = QLineEdit("")

        # Add widgets to horizontal box
        hbox6.addWidget(self.ltsv_label)
        hbox6.addWidget(self.ltsv_value)
        
        # Return all boxes
        return hbox, hbox2, hbox3, hbox4, hbox5, hbox6

    def market_widgets(self, hbox):
        self.market_label = QLabel("Mercado:")
        self.market_location = QComboBox(self)

        # Note: Use a guaranteed absolute path for robustness (recommended practice)
        DB_PATH = "./databases/products.db"
        
        # Use 'with' statement for reliable connection handling
        with sqlite3.connect(DB_PATH) as connection:
            conn_cursor = connection.cursor()

            # To select market column
            # Using DISTINCT is usually better for ComboBoxes to avoid duplicates
            statement = '''SELECT DISTINCT MARKET_LOCATION FROM products'''
            conn_cursor.execute(statement)

            # 1. FETCH THE DATA ONCE and store it in a variable
            market_data = conn_cursor.fetchall()

        # 2. ITERATE OVER THE STORED LIST
        # Python allows direct iteration over the list of tuples
        for row in market_data:
            # row is a tuple, e.g., ('Colombia',)
            self.market_location.addItem(row[0])

        # Add to widget
        hbox.addWidget(self.market_label)
        hbox.addWidget(self.market_location)
        

    def product_widgets(self, hbox):
        self.product_label = QLabel("Producto:")
        self.product_name = QComboBox(self)

        hbox.addWidget(self.product_label)
        hbox.addWidget(self.product_name)
        
    
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