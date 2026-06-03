import pyvisa
import math

import logging

logger = logging.getLogger(__name__)

class OPM:
    def __init__(self, resource_string: str, avg_count=1000) -> None:
        self.connected = False  # initialize
        logger.info(f"Opening resource: {resource_string}")

        self.rm = pyvisa.ResourceManager()
        logger.info(f"Available: {self.rm.list_resources()}")

        self.instr = self.rm.open_resource(resource_string)

        self.instr.write("SENS:RANGE:AUTO ON")
        self.instr.write("SENS:CORR:WAV 1310")
        self.instr.write("SENS:POW:UNIT W")
        self.instr.write(f"SENS:AVER {avg_count}")
        
        self.connected = True  # if we reached here, it's connected

    def read_power_dbm(self) -> float:
        """
        Retrieve measured power
        """
        power_watts = float(self.instr.query("MEAS:POW?"))

        if power_watts <= 0:
            return -100

        return 10 * math.log10(power_watts / 1e-3)

    def close(self):
        """
        Close OPM instance
        """
        self.instr.close()
        self.rm.close()
    
    def __str__(self):
        return f"Optical Power Meter {self.instr}"

