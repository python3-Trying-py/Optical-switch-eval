from app.X2OOptics.optical_switch import Switch
from app.X2OOptics.opm import OPM
from app.X2OOptics.shelf_manager import ShelfManager

import logging

logger = logging.getLogger(__name__)

class TestModel:
    def __init__(self) -> None:
        pass 
        

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
        except Exception as e:
            logger.info(f"Failed to connect to optical switch\nError: {e}")
    
    def connect_shelf(self) -> None:
        try:
            #Shelf is not changing so I am not going through that hassle
            self.shelf = ShelfManager()
            logger.info(f"Successfully connected to {self.switch}")
        except Exception as e:
            logger.info(f"Failed to connect to optical switch\nError: {e}")

    def read_optical_power(self) -> float:
        return self.opm.read_power_dbm()