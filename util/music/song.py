import os

import config


class Song:
    def __init__(self, title: str, name: str, duration: int, skip_votes: int = 1):
        self.title = title
        self.duration = duration
        self.name = name
        self.filename = os.path.abspath(f"{config.SONGS_PATH}/{name}.opus")
        self.votes = 0
        self.skip_votes = skip_votes

    def __str__(self):
        return self.title
