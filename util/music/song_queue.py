from util.music.song import Song


class SongQueue:
    def __init__(self, unique=False):
        self.queue = []
        self.unique = unique

    def add_song(self, song: Song):
        if not self.unique:
            self.queue.append(song)
        else:
            for i in range(self.current_song, self.songs):
                if self.queue[i] == song.filename:
                    return
            self.queue.append(song)

    def vote_song(self):
        s = self.queue[0]
        s.votes += 1
        if s.votes >= s.skip_votes:
            self.skip_song()

    def skip_song(self):
        res = tuple([self.current_song, self.next_song])
        del self.queue[0]
        return res

    def clear_queue(self):
        self.queue = []

    @property
    def list_songs(self):
        if self.songs == 0:
            return None
        return tuple(self.queue)

    @property
    def current_song(self):
        if self.empty:
            return None
        return self.queue[0]

    @property
    def next_song(self):
        if self.songs == 1:
            return None
        return self.queue[1]

    @property
    def songs(self):
        return len(self.queue)

    @property
    def empty(self):
        return self.songs == 0
