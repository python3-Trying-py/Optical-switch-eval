import logging

logger = logging.getLogger(__name__)

class MainController:
    def __init__(self, model, viewers):
        self.model = model
        self.viewers = viewers

        self.connect_signals()

    def connect_signals(self):
        self.viewers.OPM_confirm.clicked.connect(self.connect_opm)
        self.viewers.read_power.clicked.connect(self.display_reading)

    def connect_opm(self):
        #self.viewers.CB_fight_selection.clear()
        #for fight_title in self.model.grab_fights():
            #self.viewers.CB_fight_selection.addItem(fight_title)
        self.model.connect_OPM(self.viewers.OPM_path.text(), 1000)
    
    def display_reading(self):
        self.viewers.output_box.insertPlainText(f"Switch {self.viewers.crnt_channel.text()}: {self.model.read_optical_power()} dBm")