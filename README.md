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
