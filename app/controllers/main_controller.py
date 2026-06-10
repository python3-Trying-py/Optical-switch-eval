from typing import Callable
from functools import wraps
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from typing import Callable

import logging

logger = logging.getLogger(__name__)

class Worker(QObject):

    finished = pyqtSignal()

    def __init__(self, func: Callable[[], None]) -> None:
        super().__init__()
        self.func = func

    def run(self) -> None:
        self.func()
        self.finished.emit()

class MainController:
    def __init__(self, eval_model, background_model, viewers) -> None:
        self.eval_model = eval_model
        self.bg_model = background_model
        self.viewers = viewers

        self.connect_signals()

    def connect_signals(self) -> None:
        self.viewers.OPM_confirm.clicked.connect(self.connect_opm)
        self.viewers.switch_confirm.clicked.connect(self.connect_switch)
        self.viewers.read_power.clicked.connect(self.display_reading)
        self.viewers.prev_channel.clicked.connect(self.prev_channel)
        self.viewers.next_channel.clicked.connect(self.next_channel)
        self.viewers.save_data.clicked.connect(self.save_results)

    def connect_opm(self) -> None:
        self.eval_model.connect_OPM(self.viewers.OPM_path.text())

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
        @wraps(func)
        def wrapper(self) -> None:
            logger.debug("wrapper entered")
            self.disable_interaction()

            #Thread object allows for time.sleep()s to function within the QT event loop
            #If not done this way then the program will either brick or fail to disable and enable gui elements properly, depending on implementation
            thread = QThread()
            #Worker expects a function with no args but we need self, so run the function with self inside an anonymous function(which will then have no args), and pass that to the worker
            worker = Worker(lambda: func(self))
            worker.moveToThread(thread)

            thread.started.connect(worker.run)
            worker.finished.connect(thread.quit)
            #Dumps the worker and thread once the QT event loop has moved on from this thread, frees up memory(I think, I'm a physics student  not a compsci student)
            worker.finished.connect(worker.deleteLater)
            thread.finished.connect(thread.deleteLater)
            worker.finished.connect(self.enable_interaction)

            self._thread = thread
            self._worker = worker

            thread.start()

            logger.debug("leaving wrapper")

        return wrapper

    def connect_switch(self) -> None:
        self.eval_model.connect_switch(self.viewers.switch_path.text())
        self.viewers.crnt_channel.change_channel(1)
        self.eval_model.channel = 1
        self.eval_model.select_channel(1)
        self.viewers.show_popup_box("Please set a switch label.")

        if self.eval_model.switch_loaded == True:
            self.enable_interaction()

    def refresh_channels(self) -> None:
        """
        Refreshes channel to prevent measurement bleeding
        """
        if self.eval_model.channel == 2:
            self.eval_model.select_channel(1)
        else:
            self.eval_model.select_channel(2)

    @pause_interaction
    def prev_channel(self) -> None:
        """
        Switches to the previous channel and refreshes channel
        """
        if self.eval_model.channel == 1:
            self.viewers.output_box.insertPlainText("Switching to new optical switch\n")
            self.viewers.show_popup_box("Please connect new switch.")
            self.eval_model.channel = 43
        else:
            self.eval_model.channel = self.eval_model.channel - 1

        self.refresh_channels()

        self.eval_model.select_channel(self.eval_model.channel)
        self.viewers.crnt_channel.change_channel(self.eval_model.channel)

    @pause_interaction
    def next_channel(self) -> None:
        """
        Switches to the next channel and refreshes channel
        """
        if self.eval_model.channel == 43:
            self.viewers.output_box.insertPlainText("Switching to new optical switch\n")
            self.viewers.show_popup_box("Please connect new switch.")
            self.eval_model.channel = 1
        else:
            self.eval_model.channel = self.eval_model.channel + 1

        self.refresh_channels()

        self.eval_model.select_channel(self.eval_model.channel)
        self.viewers.crnt_channel.change_channel(self.eval_model.channel)

    def display_reading(self) -> None:
        """
        Displays current optical power to message box
        """
        channel: tuple = self.viewers.crnt_channel.get_channel()
        power: float = self.eval_model.read_optical_power(self.viewers.switch_path.text(), channel[0], channel[1])

        self.viewers.output_box.insertPlainText(f"Switch channel {channel[0]}-{channel[1]}: {power} dBm\n")

    def save_results(self) -> None:
        logger.info("Saving results")
        
        self.eval_model.save_results()

        logger.info("Results saved")