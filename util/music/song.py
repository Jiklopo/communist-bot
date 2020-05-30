import os


class Song:
    def __init__(self, title: str, filename: str, duration: int, skip_votes: int = 1):
        self.title = title
        self.duration = duration
        self.filename = os.path.abspath(f"resources/{filename}.opus")
        self.votes = 0
        self.skip_votes = skip_votes

    def __str__(self):
        return self.title
