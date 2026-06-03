from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QGridLayout, QWidget, QLabel, QTextEdit
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
        self.OPM_path: QLineEdit = QLineEdit("USB0::0x1313::0x8076::M01217675::0::INSTR")
        self.OPM_confirm: QPushButton = QPushButton("Confirm")
        
        self.switch_path: QLineEdit = QLineEdit()
        self.switch_confirm: QPushButton = QPushButton("Confirm")

        #Operation
        self.next_channel: QPushButton = QPushButton(">>")
        self.prev_channel: QPushButton = QPushButton("<<")
        self.crnt_channel: QLabel = QLabel("X-XX")
        self.read_power: QPushButton = QPushButton("Read Power")
        
        #Output
        self.output_box: QTextEdit = QTextEdit(readOnly = True)


        """
        Create and organize layout
        """
        master_layout: QGridLayout = QGridLayout()
        #Inputs
        master_layout.addWidget(self.OPM_path, 0, 0, 1, 2)
        master_layout.addWidget(self.OPM_confirm, 0, 2)
        master_layout.addWidget(self.switch_path, 1, 0, 1, 2)
        master_layout.addWidget(self.switch_confirm, 1, 2)
        #Operation
        master_layout.addWidget(self.prev_channel,2,0)
        master_layout.addWidget(self.crnt_channel,2,1)
        master_layout.addWidget(self.next_channel,2,2)
        master_layout.addWidget(self.read_power,3,1)
        #data
        master_layout.addWidget(self.output_box,4,1)

        """
        Slot everything into the GUI
        """
        # Set the central widget of the Window.
        central_widget = QWidget()
        central_widget.setLayout(master_layout)
        self.setCentralWidget(central_widget)