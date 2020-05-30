from queue import Queue
from util.music.song import Song
import os


class MusicQueue:
    def __init__(self):
        # These are guild id and path to the song queue
        self.queues = {1: Queue()}

    def add_song(self, guild_id: int, song: Song):
        if not self.queues.get(guild_id):
            self.queues[guild_id] = Queue()
        self.queues[guild_id].put(song)

    def skip_song(self, guild_id):
        q = self.queues.get(guild_id)
        if not q:
            return
        song = q.get()
        os.remove(song.filename)

    def next_song(self, guild_id):
        q = self.queues.get(guild_id)
        if not q:
            return
        return q.get()

    def vote_song(self, guild_id, song):
        pass
