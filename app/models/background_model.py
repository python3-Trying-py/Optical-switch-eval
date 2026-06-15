import pandas as pd #use pandas instead of csv because it is easier to access columns this way
from datetime import datetime
from PyQt6.QtCore import QAbstractTableModel, Qt

import logging

logger = logging.getLogger(__name__)

class ListModel(QAbstractTableModel):
    def __init__(self, data, headers=None, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers or []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal and section < len(self._headers):
                return self._headers[section]
            if orientation == Qt.Orientation.Vertical:
                return str(section)
        return None

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

class BackgroundModel:
    """
    Model which handles background logic for application not directly relating to evaluation
    """
    def __init__(self) -> None:
        self.devices: pd.dataframe = pd.read_csv("./devices.csv")

    def get_column_list(self, column) -> list:
        logger.debug(self.devices[column])
        return self.devices[column]

    def get_column_model(self, column: str) -> ListModel:
        return ListModel(self.get_column_list(column))