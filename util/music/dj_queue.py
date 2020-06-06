import os

import config as cfg
from util.music.song_queue import Song, SongQueue


class DjQueue:
    def __init__(self):
        self.queue = {1: SongQueue()}

    def add_song(self, guild, song: Song):
        if guild.id not in self.queue:
            self.queue[guild.id] = SongQueue()
        return self.queue[guild.id].add_song(song)

    def vote_song(self, guild):
        if guild.id not in self.queue:
            return
        vote = self.queue[guild.id].vote_song()
        if vote:
            os.remove(vote[0].filename)
            return vote[1]

    def skip_song(self, guild):
        if guild.id not in self.queue:
            return
        songs = self.queue[guild.id].skip_song()
        if self.song_deletable(songs[0]):
            os.remove(songs[0].filename)
        return songs[1]

    def delete_all(self, guild):
        if cfg.SAVE_SONGS:
            return
        q = self.queue.get(guild.id)
        if q:
            for s in q.queue:
                os.remove(s.filename)
            q.clear_queue()

    def song_deletable(self, song: Song):
        # TODO: Can song be deleted?
        return True

    def current_song(self, guild):
        return self.queue.get(guild.id).current_song

    def songs(self, guild):
        return self.queue.get(guild.id).queue
