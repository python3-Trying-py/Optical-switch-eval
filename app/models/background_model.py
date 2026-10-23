import pandas as pd #use pandas instead of csv because it is easier to access columns this way
from datetime import datetime
from PyQt6.QtCore import QAbstractTableModel, Qt, pyqtSlot
from PyQt6.QtWidgets import QTableWidget, QPushButton, QTableWidgetItem

import logging

logger = logging.getLogger(__name__)


class BackgroundModel:
    """
    Model which handles background logic for application not directly relating to evaluation
    """
    def __init__(self) -> None:
        self.devices: pd.dataframe = pd.read_csv("./devices.csv")
        logger.debug(self.devices)

    def get_column_list(self, column) -> list:
        logger.debug(self.devices[column])
        return self.devices[column]

    def populate_device_table(self, table: QTableWidget, column: str) -> None:
        device_list = self.get_column_list(column)
        logger.debug(f"populate_device_table: Device list: {device_list}")
        for device in device_list:
            self.add_row(table, device)
    
    def add_row(self, table: QTableWidget, text: str) -> None:
        current_row = table.rowCount()
        table.insertRow(current_row)

        text_item = QTableWidgetItem(text)

        table.setItem(current_row, 0, text_item)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda _checked, b=delete_button, t=table: self.delete_clicked(b, t))
        table.setCellWidget(current_row, 1, delete_button)

    """@pyqtSlot()
    def delete_Clicked(self):
        button = self.sender()
        if button:
            row = self.table.indexAt(button.pos()).row()
            self.table.removeRow(row)"""

    def delete_clicked(self, button: QPushButton, table: QTableWidget) -> None:
        for row in range(table.rowCount()):
            if table.cellWidget(row, 1) is button:
                table.removeRow(row)
                break
