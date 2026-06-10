import pandas as pd #use pandas instead of csv because it is easier to access columns this way
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class BackgroundModel:
    """
    Model which handles background logic for application not directly relating to evaluation
    """
    def __init__(self) -> None:
        self.devices: pd.dataframe = pd.read_csv("./devices.csv")

    def get_column_df(self, column: str) -> pd.DataFrame:
        return self.devices[column]