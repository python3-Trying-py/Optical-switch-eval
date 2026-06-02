from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QGridLayout, QWidget, QLabel
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        """
        Create all the widgets
        """
        #Inputs
        '''Needs defaults
        - Payton 06/01/2026'''
        OPM_path: QLineEdit = QLineEdit()
        OPM_confirm: QPushButton = QPushButton("Confirm")
        
        switch1_path: QLineEdit = QLineEdit()
        switch1_confirm: QPushButton = QPushButton("Confirm")

        switch2_path: QLineEdit = QLineEdit()
        switch2_confirm: QPushButton = QPushButton("Confirm")

        shelf_path: QLineEdit = QLineEdit()
        shelf_confirm: QPushButton = QPushButton("Confirm")

        #Operation
        next_channel: QPushButton = QPushButton(">>")
        prev_channel: QPushButton = QPushButton("<<")
        crnt_channel: QLabel = QLabel("X-XX")
        
        #data
        optical_power: QLabel = QLabel("Optical Power: 0")


        """
        Create and organize layout
        """
        master_layout: QGridLayout = QGridLayout()
        #Inputs
        master_layout.addWidget(OPM_path, 0, 0, 1, 2)
        master_layout.addWidget(OPM_confirm, 0, 2)
        master_layout.addWidget(switch1_path, 1, 0, 1, 2)
        master_layout.addWidget(switch1_confirm, 1, 2)
        master_layout.addWidget(switch2_path, 2, 0, 1, 2)
        master_layout.addWidget(switch2_confirm, 2, 2)
        master_layout.addWidget(shelf_path, 3, 0, 1, 2)
        master_layout.addWidget(shelf_confirm, 3, 2)
        #Operation
        master_layout.addWidget(prev_channel,4,0)
        master_layout.addWidget(crnt_channel,4,1)
        master_layout.addWidget(next_channel,4,2)
        #data
        master_layout.addWidget(optical_power,5,1)

        """
        Slot everything into the GUI
        """
        # Set the central widget of the Window.
        central_widget = QWidget()
        central_widget.setLayout(master_layout)
        self.setCentralWidget(central_widget)