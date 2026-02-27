from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGroupBox, QTableView, QLineEdit, QComboBox, QSpinBox, QScrollArea, QFrame)
from PySide6.QtCore import Qt, Slot, Signal

import sqlite3
import os

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Set Window Constraints
        self.setWindowTitle("Payout Calculator")
        self.resize(1000, 700) # Good default size for most laptops

        # Create the Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True) # Crucial: lets internal widgets resize
        scroll.setFrameShape(QFrame.NoFrame) # Makes it look seamless

        # Create the "Content Widget" that actually holds your UI
        content_widget = QWidget()
        self.window_layout = QVBoxLayout(content_widget)

        # Registries
        self.dcsv_product_reg = []
        self.pracsv_product_reg = []

        # Sections to stack
        (market_layout, dcsv_layout, prac_layout, gsv_layout, ltsv_layout, preview_layout) = self.create_layouts()

        # Stacking the sections
        self.window_layout.addWidget(market_layout)
        self.window_layout.addWidget(dcsv_layout)
        self.window_layout.addWidget(prac_layout)
        self.window_layout.addWidget(gsv_layout)
        self.window_layout.addWidget(ltsv_layout)
        self.window_layout.addWidget(preview_layout)

        # Create calc payout button and style
        self.calc_payout_button = QPushButton("Calc Payout")
        self.calc_payout_button.setStyleSheet("font-weight: bold; border: 2px solid #27ae60;")
        
        # Add calc button at the end of the layout
        self.window_layout.addWidget(self.calc_payout_button)

        # Button clicks
        self.calc_payout_button.clicked.connect(self.calculate_total_payout)
        self.dcsv_button.clicked.connect(lambda: self.add_product_row(self.dcsv_vbox2, self.dcsv_product_reg))
        self.pracsv_button.clicked.connect(lambda: self.add_product_row(self.pracsv_vbox2, self.pracsv_product_reg))

        # Set the content widget into the scroll area
        scroll.setWidget(content_widget)

        # Set the scroll area as the ONLY layout for the MainWidget
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        layout.setContentsMargins(0,0,0,0)

        self.window_layout.setSizeConstraint(QVBoxLayout.SetMinAndMaxSize)

    ############## WINDOW ELEMENTS ##############

    def create_menus(self):
        self._management_menu = self.menuBar().addMenu("&Gestionar")
        self._add_product_action = QAction("Añadir Producto")
        self._edit_product_action = QAction("Editar Producto")

        self._management_menu.addAction(self._add_product_action)
        self._management_menu.addAction(self._edit_product_action)

    
    def create_layouts(self):
        ################ Fetch DB Data ################

        self.fetch_from_db()
        print(self.products_db)

        ################ Market Layout ################

        market_layout = self.create_market_layout()

        ################ Direct Sales Layout ################

        # Create layouts
        dcsv_layout = self.create_dcsv_layout()

        # Update the comboboxes
        dcsv_combobox = self.dcsv_product_reg[0]["product_name"]
        self.populate_combobox(dcsv_combobox)

        ################ Partner Direct Sales Layout ################

        pracsv_layout = self.create_pracsv_layout()

        # Update the comboboxes
        pracsv_combobox = self.pracsv_product_reg[0]["product_name"]
        self.populate_combobox(pracsv_combobox)

        ################ Construction Bonus (GSV) Layout ################

        gsv_layout = self.create_gsv_layout()

        ################ Leadership Bonux Layout ################
        
        ltsv_layout = self.create_ltsv_layout()

        ######## Final Preview Layout ########
        
        preview_layout = self.create_preview_layout()
        
        ######## Return all layouts ########
        return market_layout, dcsv_layout, pracsv_layout, gsv_layout, ltsv_layout, preview_layout

    ############## CREATE LAYOUTS ##############

    def create_market_layout(self):
        market_vbox = QVBoxLayout()

        # Create and add widget
        self.market_combobox = QComboBox()
        for market in set(self.products_db["MARKET_LOCATION"]):
            self.market_combobox.addItem(market)
        market_vbox.addWidget(self.market_combobox)

        # Set layout
        market_layout = QGroupBox("Mercado")
        market_layout.setLayout(market_vbox)

        return market_layout
        

    def create_dcsv_layout(self):
        # Structural elements
        groupbox = QGroupBox("Ventas Directas")
        groupbox.setCheckable(True)
        groupbox.setChecked(False)

        groupbox_layout = QVBoxLayout(groupbox)

        container = QWidget()
        dcsv_vbox1 = QVBoxLayout(container)
        
        # Save the groupbox to check if toggled later
        self.dcsv_groupbox = groupbox

        # Everything inside basic_section_widgets is important to keep
        (self.dcsv_vbox2, self.dcsv_button, self.dcsv_value) = self.basic_section_widgets(
            vbox1=dcsv_vbox1,
            registry=self.dcsv_product_reg,
            value_label="DCSV:"
        )

        # Add container to layout
        groupbox_layout.addWidget(container)
        
        # Toggle logic
        container.setVisible(False)
        groupbox.toggled.connect(container.setVisible)
        
        return groupbox


    def create_pracsv_layout(self):
        # Structural elements
        groupbox = QGroupBox("Ventas Directas de Socios")
        groupbox.setCheckable(True)
        groupbox.setChecked(False)

        groupbox_layout = QVBoxLayout(groupbox)

        container = QWidget()
        pracsv_vbox1 = QVBoxLayout(container)
        
        # Save the groupbox to check if toggled later
        self.pracsv_groupbox = groupbox

        # Everything inside basic_section_widgets is important to keep
        (self.pracsv_vbox2, self.pracsv_button, self.pracsv_value) = self.basic_section_widgets(
            vbox1=pracsv_vbox1,
            registry=self.pracsv_product_reg,
            value_label="PRAC-SV:"
        )

        # Add container to layout
        groupbox_layout.addWidget(container)
        
        # Toggle logic
        container.setVisible(False)
        groupbox.toggled.connect(container.setVisible)
        
        return groupbox

    def create_gsv_layout(self):
        # Structural elements
        groupbox = QGroupBox("Volumen Grupal")
        groupbox.setCheckable(True)
        groupbox.setChecked(False)

        groupbox_layout = QVBoxLayout(groupbox)

        container = QWidget()
        gsv_vbox1 = QVBoxLayout(container)
        
        (self.basic_gsv_value, self.adm_gsv_value) = self.GSV_widgets(gsv_vbox1)

        # Add container to layout
        groupbox_layout.addWidget(container)
        
        # Toggle logic
        container.setVisible(False)
        groupbox.toggled.connect(container.setVisible)

        return groupbox


    def create_ltsv_layout(self):
        # Structural elements
        groupbox = QGroupBox("Volumen Por Liderazgo")
        groupbox.setCheckable(True)
        groupbox.setChecked(False)

        groupbox_layout = QVBoxLayout(groupbox)

        container = QWidget()
        ltsv_vbox1 = QVBoxLayout(container)
        
        self.ltsv_value = self.LTSV_widgets(ltsv_vbox1)

        # Add container to layout
        groupbox_layout.addWidget(container)
        
        # Toggle logic
        container.setVisible(False)
        groupbox.toggled.connect(container.setVisible)

        return groupbox


    def create_preview_layout(self):
        # Create vbox
        preview_vbox = QVBoxLayout()

        # Add widgets
        self.preview_widgets(preview_vbox)

        # Set layout
        preview_layout = QGroupBox("Preview")
        preview_layout.setLayout(preview_vbox)
        
        return preview_layout
    
    ############## HELPER FUNCTIONS ##############
        
    def basic_section_widgets(self, vbox1, registry, value_label:str="Value"):
        # Create vbox2
        vbox2 = QVBoxLayout()

        # Widgets
        self.add_product_row(vbox2, registry)
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

        return vbox2, button, value


    def GSV_widgets(self, vbox1):
        # Basic GSV
        basic_gsv_value = QSpinBox()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Basic GSV (DC-SV):"))
        hbox1.addWidget(basic_gsv_value)

        # AdM GSV
        adm_gsv_value = QSpinBox()
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("AdM GSV:"))
        hbox2.addWidget(adm_gsv_value)

        # Add Layouts
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)

        return basic_gsv_value, adm_gsv_value


    def LTSV_widgets(self, vbox1):
        # RdM LTSV
        ltsv_value = QSpinBox()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("LTSV:"))
        hbox1.addWidget(ltsv_value)

        # Add Layouts
        vbox1.addLayout(hbox1)

        return ltsv_value

    def preview_widgets(self, vbox1):
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
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(hbox3)
        vbox1.addLayout(hbox4)

    def populate_combobox(self, combobox):
        for product in self.products_db["PRODUCT_NAME"]:
            combobox.addItem(product)


    ############## BUTTONS ##############

    def add_product_row(self, vbox2, registry):
        # Widgets
        combo = QComboBox()
        spin = QSpinBox()
        
        # Add the widgets
        hbox1 = QHBoxLayout()
        hbox1.addWidget(combo)
        hbox1.addWidget(spin)
        vbox2.addLayout(hbox1)
        
        # Save the important data 
        row_data = {
            "product_name": combo,
            "product_quantity": spin,
        }
        registry.append(row_data)

    
    def calculate_total_payout(self):
        dcsv = float(self.preview_dcsv_value.text())
        pracsv = float(self.preview_pracsv_value.text())
        gsv = float(self.preview_gsv_value.text())
        ltsv = float(self.preview_ltsv_value.text())

        payout = dcsv + pracsv + gsv + ltsv
        print(payout)

    ############## FETCH FROM DB ##############

    def fetch_from_db(self):
        # Note: Change to a guaranteed absolute path for robustness (recommended practice)
        DB_PATH = "./src/databases/products.db"
        
        # Use 'with' statement for reliable connection handling
        with sqlite3.connect(DB_PATH) as connection:
            conn_cursor = connection.cursor()

            # To select market column
            # Using DISTINCT is usually better for ComboBoxes to avoid duplicates
            fetch_data = '''SELECT * FROM products'''
            conn_cursor.execute(fetch_data)

            # 1. FETCH THE DATA ONCE and store it in a variable
            data = conn_cursor.fetchall()

        # Variables from db columns
        sku_number = []
        market_location = []
        product_name = []

        for row in data:
            # row is a tuple
            sku_number.append(row[0])
            market_location.append(row[1])
            product_name.append(row[2])

        # Save all the data into a dictionary
        self.products_db = {"SKU": sku_number, "MARKET_LOCATION": market_location, "PRODUCT_NAME": product_name}

    def refresh_products(self):
        pass