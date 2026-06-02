import logging

logger = logging.getLogger(__name__)

class TestModel:
    def __init__(self):
        self.current_song = None
        self.is_playing = False

    def set_song(self, path):
        self.current_song = path