from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QGridLayout, QWidget, QLabel, QTextEdit, QHBoxLayout, QMessageBox, QComboBox, QTabWidget, QTableView

import logging

logger = logging.getLogger(__name__)

class channel_tracker(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.switch_label = QLineEdit("X")
        self.channel = QLabel(" - XX")
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.switch_label)
        self.layout.addWidget(self.channel)

        self.setLayout(self.layout)
    
    def change_channel(self, new_channel: int) -> None:
        """
        Changes displayed channel
        """
        self.channel.setText(f" - {new_channel}")

    def get_channel(self) -> tuple[str,int]:
        """
        Returns tuple of switch label and current channel
        """
        return self.switch_label.text(), int(self.channel.text().replace(" - ", ""))

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Optical Switch Evaluation")

        """
        Create Tabs
        """
        self.tabs = QTabWidget()
        self.eval_tab = QWidget()
        self.manage_devices_tab = QWidget()

        '''Evaluation Tab'''
        """
        Create all the widgets
        """
        #Inputs
        self.OPM_label = QLabel("OPM Connection:")
        self.OPM_path = QComboBox()
        self.OPM_confirm = QPushButton("Confirm")
        
        self.switch_label = QLabel("Switch Connection:")
        self.switch_path = QComboBox()
        self.switch_confirm = QPushButton("Confirm")

        #Operation
        self.next_channel = QPushButton(">>")
        self.prev_channel = QPushButton("<<")
        self.crnt_channel = channel_tracker()
        self.read_power = QPushButton("Read Power")

        self.next_channel.setEnabled(False)
        self.prev_channel.setEnabled(False)
        self.crnt_channel.setEnabled(False)
        self.read_power.setEnabled(False)
        
        #Data
        self.file_name = QLineEdit()
        self.save_data = QPushButton("Save Data")
        self.output_box = QTextEdit(readOnly = True)

        self.save_data.setEnabled(False)
        self.output_box.setEnabled(False)


        """
        Create and organize layout
        """
        eval_master_layout = QGridLayout()
        #Inputs
        eval_master_layout.addWidget(self.OPM_label, 0, 0)
        eval_master_layout.addWidget(self.OPM_path, 0, 1)
        eval_master_layout.addWidget(self.OPM_confirm, 0, 2)
        eval_master_layout.addWidget(self.switch_label, 1, 0)
        eval_master_layout.addWidget(self.switch_path, 1, 1)
        eval_master_layout.addWidget(self.switch_confirm, 1, 2)
        #Operation
        eval_master_layout.addWidget(self.prev_channel,2,0)
        eval_master_layout.addWidget(self.crnt_channel,2,1)
        eval_master_layout.addWidget(self.next_channel,2,2)
        eval_master_layout.addWidget(self.read_power,3,1)
        #Data
        eval_master_layout.addWidget(self.file_name,4,0)
        eval_master_layout.addWidget(self.save_data,4,1)
        eval_master_layout.addWidget(self.output_box,5,0,1,3)

        self.eval_tab.setLayout(eval_master_layout)

        '''Manger Devices Tab'''
        """
        Create all Widgets
        """
        self.saved_OPM = QTableView()
        self.saved_switch = QTableView()

        """
        Create and organize layout
        """
        manager_master_layout = QGridLayout()
        manager_master_layout.addWidget(self.saved_OPM,0,0)
        manager_master_layout.addWidget(self.saved_switch,1,0)

        self.manage_devices_tab.setLayout(manager_master_layout)

        """
        Slot everything into the GUI
        """

        self.tabs.addTab(self.eval_tab, "Evaluation")
        self.tabs.addTab(self.manage_devices_tab, "Manage Devices")

        # Set the central widget of the Window.
        self.setCentralWidget(self.tabs)

    def show_popup_box(self, message: str, title: str = "Notice", icon: str = "Info", parent = None):
        """
        Displays popup box with information
        """
        icons = {
            "Critical": QMessageBox.Icon.Critical,
            "Warning":  QMessageBox.Icon.Warning,
            "Info":     QMessageBox.Icon.Information,
            "Question": QMessageBox.Icon.Question
        }
        dialog = QMessageBox(parent)
        dialog.setIcon(icons.get(icon, QMessageBox.Icon.Critical))
        dialog.setWindowTitle(title)
        dialog.setText(message)
        dialog.exec()