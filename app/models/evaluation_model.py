from app.X2OOptics.optical_switch import Switch
from app.X2OOptics.opm import OPM
from app.X2OOptics.shelf_manager import ShelfManager

from app.X2OOptics.opm import OPM
from app.X2OOptics.optical_switch import Switch

#Test cases
#from app.X2OOptics.mock_opm import mock_OPM as OPM
#from app.X2OOptics.mock_optical_switch import mock_Switch as Switch

import csv
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class EvalModel:
    def __init__(self) -> None:
        self.channel = 1
        self.optical_switch = 'A'
        self.data:list[list[str, str, int, float]] = []
        self.switch_loaded = False  

    def connect_OPM(self, path: str, avg_count: int = 1000) -> None:
        try:
            self.opm = OPM(path, avg_count)
            logger.info(f"Successfully connected to {self.opm}")
        except Exception as e:
            logger.info(f"Failed to connect to OPM\nError: {e}")

    def connect_switch(self, path: str, channel_count: int = 43) -> None:
        try:
            self.switch = Switch(path, channel_count)
            logger.info(f"Successfully connected to {self.switch}")
            self.switch_loaded = True
        except Exception as e:
            logger.info(f"Failed to connect to optical switch\nError: {e}")
            self.switch_loaded = False
    
    def connect_shelf(self) -> None:
        try:
            #Shelf is not changing so I am not going through that hassle
            self.shelf = ShelfManager()
            logger.info(f"Successfully connected to {self.switch}")
        except Exception as e:
            logger.info(f"Failed to connect to optical switch\nError: {e}")
    
    def select_channel(self, new_channel: int) -> None:
        self.switch.select_chan(new_channel)

    def read_optical_power(self, switch_path:str, switch_label: str, channel: int) -> float:
        self.data.append([switch_path, switch_label, channel, self.opm.read_power_dbm()])
        return self.opm.read_power_dbm()
    
    def save_results(self) -> None:
        now = datetime.now()
        formatted_time = now.strftime("%Y%m%d_%H%M%S")

        with open(f"optical_switch_powers_{formatted_time}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # Write all rows at once
            writer.writerows(self.data)