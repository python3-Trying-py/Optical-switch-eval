import math
import logging
import random

logger = logging.getLogger(__name__)

class mock_OPM:
    def __init__(self, resource_string: str, avg_count=1000) -> None:
        self.connected = False
        self._resource_string = resource_string
        self._avg_count = avg_count

        # mock instrument settings
        self._wavelength = 1310
        self._unit = "W"
        self._auto_range = True

        logger.info(f"[MOCK] Opening resource: {resource_string}")
        logger.info(f"[MOCK] Available: ['{resource_string}']")
        print(f"[MOCK] OPM initialized on {resource_string} with avg_count={avg_count}")

        self.connected = True

    def read_power_dbm(self) -> float:
        """
        Returns a simulated power reading in dBm
        """
        # simulate a realistic optical power between -40 and -10 dBm
        simulated_dbm = random.uniform(-40.0, -10.0)
        logger.info(f"[MOCK] Power reading: {simulated_dbm:.4f} dBm")
        return round(simulated_dbm, 4)

    def close(self):
        """
        Simulate closing OPM instance
        """
        self.connected = False
        logger.info(f"[MOCK] OPM on {self._resource_string} closed")

    def __str__(self):
        return f"Optical Power Meter (MOCK) resource={self._resource_string}"