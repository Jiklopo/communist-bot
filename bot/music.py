from util.music.song_queue import SongQueue, Song
from discord import FFmpegOpusAudio, VoiceClient
from discord.ext import commands as cmd
import youtube_dl as yt
import os
import config as cfg


class Music(cmd.Cog):
    def __init__(self, bot: cmd.Bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': f'{cfg.SONGS_PATH}/%(id)s.opus',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': 128
            }]
        }
        self.ydl = yt.YoutubeDL(self.ydl_opts)
        self.queue = {}
        for g in self.bot.guilds:
            self.queue[g.id] = SongQueue()

    @cmd.command()
    async def anthem(self, ctx: cmd.Context):
        """Исполнить Гимн СССР в голосовом канале, в котором вы находитесь"""
        if not ctx.author.voice:
            await ctx.send('Вы не в голосовом канале!')
        q = self.queue[ctx.guild.id]
        if not q.add_song(Song('Гимн СССР', 'anthem', 1)):
            await ctx.send('Гимн Великой Державы уже в очереди.')
            return
        voice = self.find_vc(ctx.guild)
        if not voice:
            voice = await ctx.author.voice.channel.connect()
            voice.play(FFmpegOpusAudio(q.current_song.filename))

    @cmd.command()
    async def play(self, ctx: cmd.Context, link):
        """Исполнить композицию с буржуийского YouTube. Необходима ссылка."""
        if not ctx.author.voice:
            await ctx.send('Вы не в голосовом канале!')
            return
        info = self.ydl.extract_info(link, download=False)
        if info['duration'] > 600:
            await ctx.send('Видео должно быть короче 10 минут')
            return

        if not self.queue[ctx.guild.id].add_song(Song(info['title'], info['id'], info['duration'])):
            await ctx.send('Эта композиция уже есть в очереди.')
            return

        ch = ctx.author.voice.channel
        voice: VoiceClient = self.find_vc(ctx.guild)
        if not voice:
            voice = await ch.connect()

        self.ydl.download([link])

        if voice.is_playing() or voice.is_paused():
            await ctx.send(f"{info['title']!r} в очереди.")
        else:
            voice.play(FFmpegOpusAudio(self.queue[ctx.guild.id].current_song.filename), after=self.next_song)
            await ctx.send(f"Включаю {info['title']!r}.")

    def next_song(self, error=None):
        for v in self.bot.voice_clients:
            if not v.is_playing():
                songs = self.queue[v.guild.id].skip_song()
                if songs[0].title != 'Гимн СССР':
                    os.remove(songs[0].filename)
                if not songs[1]:
                    return
                v.play(FFmpegOpusAudio(songs[1].filename), after=self.next_song)

    @cmd.command()
    async def pause(self, ctx: cmd.Context):
        """Поставить текущий трек на паузу"""
        v = self.find_vc(ctx.guild)
        if not v:
            await ctx.send('Я не в голосовом канале.')
        elif v.is_playing():
            v.pause()
            await ctx.send('Поставил на паузу.')
        elif v.is_paused():
            await ctx.send('Уже на паузе.')
        else:
            await ctx.send('Ничего не играет.')

    @cmd.command()
    async def resume(self, ctx: cmd.Context):
        """Продолжить трек, поставленный на паузу ранее."""
        v = self.find_vc(ctx.guild)
        if not v:
            await ctx.send('Я не в голосовом канале.')
        elif v.is_paused():
            v.resume()
            await ctx.send('Продолжил трек.')
        elif v.is_playing():
            await ctx.send('Трек уже играет.')
        else:
            await ctx.send('Ничего не играет.')

    @cmd.command()
    async def stop(self, ctx: cmd.Context):
        """Остановить текущий трек и очистить очередь."""
        v = self.find_vc(ctx.guild)
        if not v:
            await ctx.send('Я не в голосовом канале.')
        elif v.is_paused() or v.is_playing():
            v.stop()
            self.delete_all_songs([ctx.guild])
        else:
            await ctx.send('Ничего не играет.')
        await v.disconnect()

    @cmd.command()
    async def skip(self, ctx: cmd.Context):
        """Пропустить текущий трек."""
        q = self.queue[ctx.guild.id]
        songs = [q.current_song, q.next_song]
        v: VoiceClient = self.find_vc(ctx.guild)
        v.stop()
        await ctx.send(f'Пропускаю {songs[0]}.')
        if not songs[1]:
            await ctx.send('В очереди не осталось песен.')
            return
        v.play(FFmpegOpusAudio(songs[1].filename), after=self.next_song)
        await ctx.send(f'Включаю {songs[1]}.')

    @cmd.command()
    async def list(self, ctx: cmd.Context):
        """Посмотреть список композиций."""
        song_list = self.queue[ctx.guild.id].list_songs
        ans = ''
        if not song_list:
            ans = 'Список композиций пуст.'
        else:
            for i, v in enumerate(song_list):
                ans += f"{i + 1}. {v.title}\n"
        await ctx.send(ans)

    def find_vc(self, guild):
        for v in self.bot.voice_clients:
            if v.guild == guild:
                return v

    def delete_songs(self, songs: [Song]):
        if cfg.SAVE_SONGS:
            return
        for s in songs:
            if s.title == 'Гимн СССР':
                continue
            os.remove(s.filename)

    def delete_all_songs(self, guilds):
        if cfg.SAVE_SONGS:
            return
        for g in guilds:
            q = self.queue.get(g.id)
            if q:
                for s in q.queue:
                    os.remove(s.filename)
                q.clear_queue()
