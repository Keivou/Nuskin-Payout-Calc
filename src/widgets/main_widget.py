from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
QPushButton, QGroupBox, QTableView, QLineEdit, QComboBox, QSpinBox)
from PySide6.QtCore import Qt, Slot, Signal

import sqlite3

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Overall vertical layout
        vertical_layout = QVBoxLayout(self)

        # Sections to stack
        (market_layout, ds_layout, prac_layout, gsv_layout, ltsv_layout, preview_layout) = self.create_layouts()

        # Stacking the sections
        vertical_layout.addWidget(market_layout)
        vertical_layout.addWidget(ds_layout)
        vertical_layout.addWidget(prac_layout)
        vertical_layout.addWidget(gsv_layout)
        vertical_layout.addWidget(ltsv_layout)
        vertical_layout.addWidget(preview_layout)

        # Adding button
        self.calc_button = self.calculate_total_payout()
        vertical_layout.addWidget(self.calc_button)

        # Setting the layout for the window
        self.setLayout(vertical_layout)

        # Button doesn't exist yet
        self.calc_button.clicked.connect(self.calculate_total_payout)

    ############## WINDOW ELEMENTS ##############

    def create_menus(self):
        self._management_menu = self.menuBar().addMenu("&Gestionar")
        self._management_menu.addAction(self._add_product_action)
        self._management_menu.addAction(self._edit_product_action)

    def create_actions(self):
        self._add_product_action = QAction("Añadir Producto", self)
        self._edit_product_action = QAction("Editar Producto", self)
    
    def create_layouts(self):
        ######## Market Layout ########
        market_vbox = QVBoxLayout()

        # Add widgets
        self.market_widgets(market_vbox)

        # Set layout
        market_layout = QGroupBox("Mercado")
        market_layout.setLayout(market_vbox)

        ######## Direct Sales Layout ########
        ds_vbox = QVBoxLayout()

        # Add widgets
        self.DC_SV_widgets(ds_vbox)

        # Set layout
        ds_layout = QGroupBox("Ventas Directas")
        ds_layout.setLayout(ds_vbox)
        ds_layout.setCheckable(True)
        ds_layout.setChecked(False)

        ######## Partner Direct Sales Layout ########
        prac_vbox = QVBoxLayout()

        # Add widgets
        self.PRAC_SV_widgets(prac_vbox)

        # Set layout
        prac_layout = QGroupBox("Ventas De Socios Directos")
        prac_layout.setLayout(prac_vbox)
        prac_layout.setCheckable(True)
        prac_layout.setChecked(False)

        ######## Construction Bonus (GSV) Layout ########
        gsv_vbox = QVBoxLayout()

        # Add widgets
        self.GSV_widgets(gsv_vbox)

        # Set layout
        gsv_layout = QGroupBox("Bono Constructor")
        gsv_layout.setLayout(gsv_vbox)
        gsv_layout.setCheckable(True)
        gsv_layout.setChecked(False)

        ######## Leadership Bonux Layout ########
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
        return market_layout, ds_layout, prac_layout, gsv_layout, ltsv_layout, preview_layout

    ############## WIDGETS ##############

    def market_widgets(self, market_vbox):
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
        market_vbox.addWidget(self.market_location)
        

    def product_widgets(self, vbox):
        # Product Name
        hbox1 = QHBoxLayout()

        self.product_label = QLabel("Producto:")
        self.product_name = QComboBox(self)

        hbox1.addWidget(self.product_label)
        hbox1.addWidget(self.product_name)

        # Product Quantity
        hbox2 = QHBoxLayout()

        self.quantity_label = QLabel("Cantidad:")
        self.quantity_value = QSpinBox()

        hbox2.addWidget(self.quantity_label)
        hbox2.addWidget(self.quantity_value)

        # Add Layouts
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)


    def DC_SV_widgets(self, vbox):
        # Products
        self.product_widgets(vbox)
        self.add_product_button(vbox)

        # DC-SV
        hbox1 = QHBoxLayout()

        self.dcsv_label = QLabel("DC-SV:")
        self.dcsv_value = QSpinBox()

        hbox1.addWidget(self.dcsv_label)
        hbox1.addWidget(self.dcsv_value)

        # Add Layouts
        vbox.addLayout(hbox1)


    def PRAC_SV_widgets(self, vbox):
        # Products
        self.product_widgets(vbox)
        self.add_product_button(vbox)

        # PRAC-SV
        hbox1 = QHBoxLayout()

        self.pracsv_label = QLabel("PRAC-SC:")
        self.pracsv_value = QSpinBox()

        hbox1.addWidget(self.pracsv_label)
        hbox1.addWidget(self.pracsv_value)

        # Add Layouts
        vbox.addLayout(hbox1)

    def GSV_widgets(self, vbox):
        # Basic GSV
        hbox1 = QHBoxLayout()

        self.basic_gsv_label = QLabel("Basic GSV (DC-SV):")
        self.basic_gsv_value = QSpinBox()

        hbox1.addWidget(self.basic_gsv_label)
        hbox1.addWidget(self.basic_gsv_value)

        # AdM GSV
        hbox2 = QHBoxLayout()

        self.adm_gsv_label = QLabel("AdM GSV:")
        self.adm_gsv_value = QSpinBox()

        hbox2.addWidget(self.adm_gsv_label)
        hbox2.addWidget(self.adm_gsv_value)

        # Add Layouts
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)


    def LTSV_widgets(self, vbox):
        # RdM LTSV
        hbox1 = QHBoxLayout()
        
        self.ltsv_label = QLabel("LTSV:")
        self.ltsv_value = QSpinBox()

        hbox1.addWidget(self.ltsv_label)
        hbox1.addWidget(self.ltsv_value)

        # Add Layouts
        vbox.addLayout(hbox1)

    def preview_widgets(self, vbox):
        # DC-SV
        hbox1 = QHBoxLayout()
        self.preview_dcsv_value = QSpinBox()

        hbox1.addWidget(QLabel("DC-SV:"))
        hbox1.addWidget(self.preview_dcsv_value)

        # PRAC-SV
        hbox2 = QHBoxLayout()
        self.preview_pracsv_value = QSpinBox()

        hbox2.addWidget(QLabel("PRAC-SV:"))
        hbox2.addWidget(self.preview_pracsv_value)

        # GSV
        hbox3 = QHBoxLayout()
        self.preview_gsv_value = QSpinBox()

        hbox3.addWidget(QLabel("GSV:"))
        hbox3.addWidget(self.preview_gsv_value)

        # LTSV
        hbox4 = QHBoxLayout()
        self.preview_ltsv_value = QSpinBox()

        hbox4.addWidget(QLabel("LTSV:"))
        hbox4.addWidget(self.preview_ltsv_value)

        # Add Layouts
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)


    ############## BUTTONS ##############

    def add_product_button(self, vbox):
        button = QPushButton("Añadir Producto")
        vbox.addWidget(button)
    

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