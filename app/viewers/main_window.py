from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QGridLayout, QWidget, QLabel, QTextEdit, QHBoxLayout, QMessageBox
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

        self.setWindowTitle("My App")

        """
        Create all the widgets
        """
        #Inputs
        self.OPM_label = QLabel("OPM Connection:")
        self.OPM_path = QLineEdit("USB0::0x1313::0x8076::M01217675::0::INSTR")
        self.OPM_confirm = QPushButton("Confirm")
        
        self.switch_label = QLabel("Switch Connection:")
        self.switch_path= QLineEdit("USB0::0x2727::0x8076::M01217456::0::3")
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
        self.save_data = QPushButton("Save Data")
        self.output_box = QTextEdit(readOnly = True)

        self.save_data.setEnabled(False)
        self.output_box.setEnabled(False)


        """
        Create and organize layout
        """
        master_layout: QGridLayout = QGridLayout()
        #Inputs
        master_layout.addWidget(self.OPM_label, 0, 0)
        master_layout.addWidget(self.OPM_path, 0, 1)
        master_layout.addWidget(self.OPM_confirm, 0, 2)
        master_layout.addWidget(self.switch_label, 1, 0)
        master_layout.addWidget(self.switch_path, 1, 1)
        master_layout.addWidget(self.switch_confirm, 1, 2)
        #Operation
        master_layout.addWidget(self.prev_channel,2,0)
        master_layout.addWidget(self.crnt_channel,2,1)
        master_layout.addWidget(self.next_channel,2,2)
        master_layout.addWidget(self.read_power,3,1)
        #Data
        master_layout.addWidget(self.save_data,4,1)
        master_layout.addWidget(self.output_box,5,0,1,3)

        """
        Slot everything into the GUI
        """
        # Set the central widget of the Window.
        central_widget = QWidget()
        central_widget.setLayout(master_layout)
        self.setCentralWidget(central_widget)

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