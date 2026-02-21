from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
QPushButton, QGroupBox, QTableView, QLineEdit, QComboBox, QSpinBox)
from PySide6.QtCore import Qt, Slot, Signal

import sqlite3
import os

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Overall vertical layout
        vertical_layout = QVBoxLayout(self)

        # Sections to stack
        (market_layout, dcsv_layout, prac_layout, gsv_layout, ltsv_layout, preview_layout) = self.create_layouts()

        # Stacking the sections
        vertical_layout.addWidget(market_layout)
        vertical_layout.addWidget(dcsv_layout)
        vertical_layout.addWidget(prac_layout)
        vertical_layout.addWidget(gsv_layout)
        vertical_layout.addWidget(ltsv_layout)
        vertical_layout.addWidget(preview_layout)

        # Create calc payout button and style
        self.calc_payout_button = QPushButton("Calc Payout")
        self.calc_payout_button.setStyleSheet("font-weight: bold; border: 2px solid #27ae60;")
        
        # Add calc button at the end of the layout
        vertical_layout.addWidget(self.calc_payout_button)

        # Setting the layout for the window
        self.setLayout(vertical_layout)

        # Button clicks
        self.calc_payout_button.clicked.connect(self.calculate_total_payout)
        self.dcsv_button.clicked.connect(self.product_widgets(self.dcsv_button))
        self.pracsv_button.clicked.connect(self.product_widgets(self.pracsv_button))

    ############## WINDOW ELEMENTS ##############

    def create_menus(self):
        self._management_menu = self.menuBar().addMenu("&Gestionar")
        self._add_product_action = QAction("Añadir Producto")
        self._edit_product_action = QAction("Editar Producto")

        self._management_menu.addAction(self._add_product_action)
        self._management_menu.addAction(self._edit_product_action)

    
    def create_layouts(self):
        ################ Market Layout ################
        self.market_vbox = QVBoxLayout()

        # Add widgets
        self.market_widgets(self.market_vbox)

        # Set layout
        self.market_layout = QGroupBox("Mercado")
        self.market_layout.setLayout(self.market_vbox)

        ################ Direct Sales Layout ################

        # Create GroupBox
        self.dcsv_layout = QGroupBox("Ventas Directas")
        self.dcsv_layout.setCheckable(True)
        self.dcsv_layout.setChecked(False)

        # Create First vbox layer
        group_vbox = QVBoxLayout(self.dcsv_layout) # Parent is the groupbox, alternative to using setLayout

        # Create a CONTAINER widget to hold the actual content
        self.dcsv_container = QWidget()
        self.dcsv_vbox1 = QVBoxLayout(self.dcsv_container) # This would be vbox1

        # Create vbox2 and vbox3 and add them to vbox1
        (self.dcsv_vbox2, self.dcsv_vbox3, self.dcsv_button, self.dcsv_value) = self.basic_section_widgets(vbox1=self.dcsv_vbox1, value_label="DCSV:")
        self.dcsv_vbox1.addLayout(self.dcsv_vbox2)
        self.dcsv_vbox1.addLayout(self.dcsv_vbox3)

        # Add the container to the GroupBox
        group_vbox.addWidget(self.dcsv_container)

        # Hide the container initially
        self.dcsv_container.setVisible(False)

        # CONNECT the signal
        self.dcsv_layout.toggled.connect(self.dcsv_container.setVisible)

        ################ Partner Direct Sales Layout ################

        # Create GroupBox
        self.pracsv_layout = QGroupBox("Ventas Directas")
        self.pracsv_layout.setCheckable(True)
        self.pracsv_layout.setChecked(False)

        # Create First vbox layer
        group_vbox = QVBoxLayout(self.pracsv_layout) # Parent is the groupbox, alternative to using setLayout

        # Create a CONTAINER widget to hold the actual content
        self.pracsv_container = QWidget()
        self.pracsv_vbox1 = QVBoxLayout(self.pracsv_container) # This would be vbox1

        # Create vbox2 and vbox3 and add them to vbox1
        (self.pracsv_vbox2, self.pracsv_vbox3, self.pracsv_button, self.pracsv_value) = self.basic_section_widgets(vbox1=self.pracsv_vbox1, value_label="DCSV:")
        self.pracsv_vbox1.addLayout(self.pracsv_vbox2)
        self.pracsv_vbox1.addLayout(self.pracsv_vbox3)

        # Add the container to the GroupBox
        group_vbox.addWidget(self.pracsv_container)

        # Hide the container initially
        self.pracsv_container.setVisible(False)

        # CONNECT the signal
        self.pracsv_layout.toggled.connect(self.pracsv_container.setVisible)

        ################ Construction Bonus (GSV) Layout ################

        self.gsv_vbox = QVBoxLayout()

        # Add widgets
        self.GSV_widgets(self.gsv_vbox)

        # Set layout
        gsv_layout = QGroupBox("Bono Constructor")
        gsv_layout.setLayout(self.gsv_vbox)
        gsv_layout.setCheckable(True)
        gsv_layout.setChecked(False)

        ################ Leadership Bonux Layout ################
        ltsv_vbox = QVBoxLayout()

        # Add widgets
        self.LTSV_widgets(ltsv_vbox)

        # Set layout
        ltsv_layout = QGroupBox("Bono Por Liderazgo")
        ltsv_layout.setLayout(ltsv_vbox)
        ltsv_layout.setCheckable(True)
        ltsv_layout.setChecked(False)

        ######## Final Preview Layout ########
        preview_vbox = QVBoxLayout()

        # Add widgets
        self.preview_widgets(preview_vbox)

        # Set layout
        preview_layout = QGroupBox("Preview")
        preview_layout.setLayout(preview_vbox)
        
        ######## Return all layouts ########
        return self.market_layout, self.dcsv_layout, self.pracsv_layout, gsv_layout, ltsv_layout, preview_layout

    ############## WIDGETS ##############

    def market_widgets(self, market_vbox):
        self.market_location = QComboBox(self)

        # Note: Use a guaranteed absolute path for robustness (recommended practice)
        DB_PATH = "./src/databases/products.db"
        
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
        market_vbox.addWidget(self.market_location)
        

    def product_widgets(self, vbox1):
        # Create vbox2
        vbox2 = QVBoxLayout()

        # Product Name
        product_name = QComboBox(self)

        # Note: Use a guaranteed absolute path for robustness (recommended practice)
        DB_PATH = "./src/databases/products.db"
        
        # Use 'with' statement for reliable connection handling
        with sqlite3.connect(DB_PATH) as connection:
            conn_cursor = connection.cursor()

            # To select market column
            # Using DISTINCT is usually better for ComboBoxes to avoid duplicates
            statement = '''SELECT DISTINCT PRODUCT_DESCRIPTION FROM products'''
            conn_cursor.execute(statement)

            # 1. FETCH THE DATA ONCE and store it in a variable
            products = conn_cursor.fetchall()

        # 2. ITERATE OVER THE STORED LIST
        # Python allows direct iteration over the list of tuples
        for row in products:
            # row is a tuple, e.g., ('Colombia',)
            product_name.addItem(row[0])

        # Product Quantity
        quantity_value = QSpinBox()
        
        # Add widgets to hbox
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Producto:"))
        hbox1.addWidget(product_name)
        hbox1.addWidget(QLabel("Cantidad:"))
        hbox1.addWidget(quantity_value)

        # Add Layouts
        inner_vbox.addLayout(hbox1)
        outer_vbox.addLayout(inner_vbox)
        
        return inner_vbox, product_name, quantity_value


    def basic_section_widgets(self, vbox1, value_label:str="Value"):
        # Widgets
        vbox2 = self.product_widgets(vbox1)
        button = QPushButton("Añadir Producto")
        value = QSpinBox()

        # Add to hbox
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel(value_label))
        hbox1.addWidget(value)

        # Create vbox3
        vbox3 = QVBoxLayout()
        vbox3.addWidget(button)
        vbox3.addLayout(hbox1)

        # Place vbox2 and vbox3 inside vbox1
        vbox1.addLayout(vbox2)
        vbox1.addLayout(vbox3)

        return vbox2, vbox3, button, value


    def GSV_widgets(self, vbox):
        # Basic GSV
        self.basic_gsv_value = QSpinBox()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Basic GSV (DC-SV):"))
        hbox1.addWidget(self.basic_gsv_value)

        # AdM GSV
        self.adm_gsv_value = QSpinBox()
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("AdM GSV:"))
        hbox2.addWidget(self.adm_gsv_value)

        # Add Layouts
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)


    def LTSV_widgets(self, vbox):
        # RdM LTSV
        self.ltsv_value = QSpinBox()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("LTSV:"))
        hbox1.addWidget(self.ltsv_value)

        # Add Layouts
        vbox.addLayout(hbox1)

    def preview_widgets(self, vbox):
        # DC-SV
        self.preview_dcsv_value = QSpinBox()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("DC-SV:"))
        hbox1.addWidget(self.preview_dcsv_value)

        # PRAC-SV
        self.preview_pracsv_value = QSpinBox()
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("PRAC-SV:"))
        hbox2.addWidget(self.preview_pracsv_value)

        # GSV
        self.preview_gsv_value = QSpinBox()
        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel("GSV:"))
        hbox3.addWidget(self.preview_gsv_value)

        # LTSV
        self.preview_ltsv_value = QSpinBox()
        hbox4 = QHBoxLayout()
        hbox4.addWidget(QLabel("LTSV:"))
        hbox4.addWidget(self.preview_ltsv_value)

        # Add Layouts
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)


    ############## CALCULATION LOGIC ##############
    
    def calculate_total_payout(self):
        dcsv = float(self.preview_dcsv_value.text())
        pracsv = float(self.preview_pracsv_value.text())
        gsv = float(self.preview_gsv_value.text())
        ltsv = float(self.preview_ltsv_value.text())

        payout = dcsv + pracsv + gsv + ltsv
        print(payout)
