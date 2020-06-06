import youtube_dl as yt
from discord import FFmpegOpusAudio, VoiceClient
from discord.ext import commands as cmd

import config as cfg
from util.music.dj_queue import DjQueue
from util.music.song_queue import Song


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
        self.queue = DjQueue()

    @cmd.command()
    async def anthem(self, ctx: cmd.Context):
        """Исполнить Гимн СССР в голосовом канале, в котором вы находитесь"""
        if not ctx.author.voice:
            await ctx.send('Вы не в голосовом канале!')
        if not self.queue.add_song(ctx.guild, Song('Гимн СССР', 'anthem', 1)):
            await ctx.send('Гимн Великой Державы уже в очереди.')
        else:
            voice = self.find_vc(ctx.guild)
            if not voice:
                voice = await ctx.author.voice.channel.connect()
                voice.play(FFmpegOpusAudio(self.queue.current_song(ctx.guild)))

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

        if not self.queue.add_song(ctx.guild, Song(info['title'], info['id'], info['duration'])):
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
            voice.play(FFmpegOpusAudio(self.queue.current_song(ctx.guild).filename), after=self.next_song)
            await ctx.send(f"Включаю {info['title']!r}.")

    def next_song(self, error=None):
        for v in self.bot.voice_clients:
            if not v.is_playing():
                song = self.queue.skip_song(v.guild)
                if not song:
                    continue
                v.play(FFmpegOpusAudio(song.filename), after=self.next_song)

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
            self.queue.delete_all(ctx.guild)
        else:
            await ctx.send('Ничего не играет.')
        await v.disconnect()

    @cmd.command()
    async def skip(self, ctx: cmd.Context):
        """Пропустить текущий трек."""
        s = self.queue.skip_song(ctx.guild)
        v: VoiceClient = self.find_vc(ctx.guild)
        v.stop()
        await ctx.send(f'Следующий трек.')
        if not s:
            await ctx.send('В очереди не осталось песен.')
        else:
            v.play(FFmpegOpusAudio(s.filename), after=self.next_song)
            await ctx.send(f'Включаю {s}.')

    @cmd.command()
    async def list(self, ctx: cmd.Context):
        """Посмотреть список композиций."""
        song_list = self.queue.songs(ctx.guild)
        ans = ''
        if not song_list:
            ans = 'Список композиций пуст.'
        else:
            for i, v in enumerate(song_list):
                ans += f"{i + 1}. {v}\n"
        await ctx.send(ans)

    def find_vc(self, guild):
        for v in self.bot.voice_clients:
            if v.guild == guild:
                return v
