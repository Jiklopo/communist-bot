import os


class Song:
    def __init__(self, title, filename, duration):
        self.title = title
        self.duration = duration
        self.filename = os.path.abspath(f"resources/{filename}.opus")
