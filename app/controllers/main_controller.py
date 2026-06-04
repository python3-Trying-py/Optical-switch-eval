from typing import Callable
from functools import wraps

import logging

logger = logging.getLogger(__name__)

class MainController:
    def __init__(self, model, viewers) -> None:
        self.model = model
        self.viewers = viewers

        self.connect_signals()

    def connect_signals(self) -> None:
        self.viewers.OPM_confirm.clicked.connect(self.connect_opm)
        self.viewers.switch_confirm.clicked.connect(self.connect_switch)
        self.viewers.read_power.clicked.connect(self.display_reading)
        self.viewers.prev_channel.clicked.connect(self.prev_channel)
        self.viewers.next_channel.clicked.connect(self.next_channel)

    def connect_opm(self) -> None:
        self.model.connect_OPM(self.viewers.OPM_path.text())

    def disable_interaction(self) -> None:
        self.viewers.next_channel.setEnabled(False)
        self.viewers.prev_channel.setEnabled(False)
        self.viewers.crnt_channel.setEnabled(False)
        self.viewers.read_power.setEnabled(False)
        self.viewers.save_data.setEnabled(False)
        self.viewers.output_box.setEnabled(False)

    def enable_interaction(self) -> None:
        self.viewers.next_channel.setEnabled(True)
        self.viewers.prev_channel.setEnabled(True)
        self.viewers.crnt_channel.setEnabled(True)
        self.viewers.read_power.setEnabled(True)
        self.viewers.save_data.setEnabled(True)
        self.viewers.output_box.setEnabled(True)

    @staticmethod
    def pause_interaction(func: Callable[[], None]) -> Callable[[], None]:
        """
        Decorator that temporily disables interaction with GUI elements related to switching channels
        """
        logger.info("Decorator entered")
        @wraps(func)
        def wrapper(self) -> None:
            logger.info("wrapper entered")
            self.disable_interaction()
            try:
                func(self)
            finally:
                self.enable_interaction()
        logger.info("wrapper left")
        return wrapper

    def connect_switch(self) -> None:
        self.model.connect_switch(self.viewers.switch_path.text())
        self.viewers.crnt_channel.change_channel(1)
        self.viewers.show_popup_box("Please set a switch label.")

        if self.model.switch_loaded == True:
            self.enable_interaction()

    def refresh_channels(self) -> None:
        """
        Refreshes channel to prevent measurement bleeding
        """
        if self.model.channel == 43:
            self.model.select_channel(1)
        else:
            self.model.select_channel(43)

    @pause_interaction
    def prev_channel(self) -> None:
        """
        Switches to the previous channel and refreshes channel
        """
        if self.model.channel == 1:
            self.viewers.output_box.insertPlainText("Switching to new optical switch\n")
            self.viewers.show_popup_box("Please set a new switch label.")
            self.model.channel = 43
        else:
            self.model.channel = self.model.channel - 1

        self.refresh_channels()

        self.model.select_channel(self.model.channel)
        self.viewers.crnt_channel.change_channel(self.model.channel)

    @pause_interaction
    def next_channel(self) -> None:
        """
        Switches to the next channel and refreshes channel
        """
        if self.model.channel == 43:
            self.viewers.output_box.insertPlainText("Switching to new optical switch\n")
            self.viewers.show_popup_box("Please set a new switch label.")
            self.model.channel = 1
        else:
            self.model.channel = self.model.channel + 1

        self.refresh_channels()

        self.model.select_channel(self.model.channel)
        self.viewers.crnt_channel.change_channel(self.model.channel)

    def display_reading(self) -> None:
        """
        Displays current optical power to message box
        """
        channel: tuple = self.viewers.crnt_channel.get_channel()
        power: float = self.model.read_optical_power(self.viewers.switch_path.text(), channel[0], channel[1])

        self.viewers.output_box.insertPlainText(f"Switch channel {channel[0]}-{channel[1]}: {power} dBm\n")