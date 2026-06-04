import time

import logging

logger = logging.getLogger(__name__)

class mock_Switch():
    """
    Mock Optical switch object - simulates hardware without serial connection
    """
    SWITCH_SLEEP_CALIB = None
    SWITCH_SLEEP_SELECT = None

    def __init__(self, dev_path: str, num_of_chans: int) -> None:
        self.path = dev_path
        self.current_chan = None
        self.switch_type = num_of_chans
        self._is_open = True  # simulate an open serial port
        logger.info(f"[MOCK] Switch initialized on {dev_path} with {num_of_chans} channels")

    def select_chan(self, chan: int) -> int:
        """
        Simulates changing current channel
        """
        if chan <= 0:
            raise ValueError("Invalid channel passed to the switch: %d" % chan)

        if chan > self.switch_type:
            raise ValueError("Channel %d exceeds switch capacity of %d" % (chan, self.switch_type))

        # simulate sleep times based on switch type (shortened for mock)
        if self.switch_type == 8:
            sleep_time = 2
        elif self.switch_type == 32:
            sleep_time = 3
        else:
            sleep_time = 2

        logger.info(f"[MOCK] Calibrating switch...")
        time.sleep(sleep_time)
        logger.info(f"[MOCK] Selecting channel {chan}...")
        time.sleep(sleep_time)

        self.current_chan = chan
        logger.info(f"[MOCK] Channel set to {chan}")
        return 0

    def get_current_chan(self):
        """
        Retrieves current channel
        """
        return self.current_chan

    def __str__(self):
        return f"Switch (MOCK) path={self.path}, type={self.switch_type}"