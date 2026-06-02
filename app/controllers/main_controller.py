import logging

logger = logging.getLogger(__name__)

class MainController:
    def __init__(self, model, viewers):
        self.model = model
        self.viewers = viewers

        self.connect_signals()
        self.update()

    def connect_signals(self):
        self.viewers.PB_play_button.clicked.connect(self.handle_play)
        self.viewers.PB_stop_button.clicked.connect(self.handle_stop)
        self.viewers.PB_fight_select.clicked.connect(self.load_fight)
        self.viewers.Ti_music_timer.timeout.connect(self.check_music)
        self.audio.intro_finished.connect(self.play_next_track)
        self.audio.fight_finished.connect(self.handle_stop)

    def update(self):
        self.viewers.CB_fight_selection.clear()
        for fight_title in self.model.grab_fights():
            self.viewers.CB_fight_selection.addItem(fight_title)