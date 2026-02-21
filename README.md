# Project Info

See on ipad

# main_widget.py

## Groupbox logic

```python
# 1. Create GroupBox
self.ds_layout = QGroupBox("Ventas Directas")
self.ds_layout.setCheckable(True)
self.ds_layout.setChecked(False)

# 2. Create a main layout for the GroupBox
group_vbox = QVBoxLayout(self.ds_layout)

# 3. Create a CONTAINER widget to hold the actual content
self.ds_container = QWidget()
self.ds_container_layout = QVBoxLayout(self.ds_container)

# 4. Add your actual widgets to the CONTAINER
self.product_widgets(self.ds_container_layout)

# 5. Add the container to the GroupBox
group_vbox.addWidget(self.ds_container)

# 6. Hide the container initially
self.ds_container.setVisible(False)

# 7. CONNECT the signal
self.ds_layout.toggled.connect(self.ds_container.setVisible)
```

## Data fetching

This avoids constantly revisiting the db and trying to fetch inside the layout creation

- Initialize Data: Query the database once and build the self.market_catalog dictionary.
- Build UI: Create the Market ComboBox and the Product ComboBoxes.
- Initial Load: Call self.update_product_list(self.market_location.currentText()) once so the app doesn't start with an empty product list.
- Connect Signal: self.market_location.currentTextChanged.connect(self.update_product_list).
