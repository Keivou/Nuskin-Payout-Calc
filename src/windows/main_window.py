from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PySide6.QtCore import Slot, QFile, Qt, QTextStream

class MainWindow(QMainWindow):

    def __init__(self, widget):

        # ------------------------------------------------------------------
        #                               INIT
        # ------------------------------------------------------------------

        super().__init__()
        self.setWindowTitle("Nu Skin Payout Calculator")
        self.main_widget = widget
        self.setCentralWidget(self.main_widget)

        # Menu
        self.menu = self.menuBar()
        self.management_menu = self.menu.addMenu("Gestionar")
        self.help_manu = self.menu.addMenu("Ayuda")
