from util.music.music_queue import MusicQueue, Song
from discord import FFmpegOpusAudio, VoiceClient
from discord.ext import commands as cmd
import youtube_dl as yt
import os
import time


class Music(cmd.Cog):
    def __init__(self, bot: cmd.Bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'resources/%(id)s.opus',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': 128
            }]
        }
        self.ydl = yt.YoutubeDL(self.ydl_opts)
        self.queue = MusicQueue()

    @cmd.command()
    async def anthem(self, ctx: cmd.Context):
        """Исполнить Гимн СССР в голосовом канале, в котором вы находитесь"""
        if not ctx.author.voice:
            await ctx.send('Вы не в голосовом канале!')
        voice = self.find_vc(ctx.guild)
        anthem = os.path.abspath('resources/anthem.opus')
        if not voice:
            ch = ctx.author.voice.channel
            voice = await ch.connect()
            voice.play(FFmpegOpusAudio(anthem))
            return
        if voice.is_playing():
            await ctx.send('Гимн поставлен в очередь.')
            self.queue.add_song(ctx.guild.id, Song('Гимн СССР', 'anthem', 0))

    @cmd.command()
    async def play(self, ctx: cmd.Context, link):
        if not ctx.author.voice:
            await ctx.send('Вы не в голосовом канале!')
            return
        ch = ctx.author.voice.channel
        voice: VoiceClient = self.find_vc(ctx.guild)
        if not voice:
            voice = await ch.connect()
        info = self.ydl.extract_info(link, download=False)
        if info['duration'] > 600:
            await ctx.send('Видео должно быть короче 10 минут')
            return
        self.ydl.download([link])
        if voice.is_playing() or voice.is_paused():
            self.queue.add_song(voice.guild.id, Song(info['title'], info['id'], info['duration']))
            await ctx.send(f"{info['title']} в очереди.")
        else:
            print(time.time())
            voice.play(FFmpegOpusAudio(f"resources/{info['id']}.opus"), after=self.next_song)

    def next_song(self, error=None):
        for v in self.bot.voice_clients:
            if not v.is_playing():
                song = self.queue.next_song(v.guild.id)
                v.play(FFmpegOpusAudio(song.filename), after=self.next_song)

    @cmd.command()
    async def pause(self, ctx: cmd.Context):
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
        v = self.find_vc(ctx.guild)
        if not v:
            await ctx.send('Я не в голоовом канале.')
        elif v.is_paused() or v.is_playing():
            v.stop()
        else:
            await ctx.send('Ничего не играет.')

    @cmd.command()
    async def skip(self, ctx: cmd.Context):
        await ctx.send('Следующая песня.')
        v: VoiceClient = self.find_vc(ctx.guild)
        v.stop()
        song = self.queue.next_song(v.guild.id)
        v.play(FFmpegOpusAudio(song.filename), after=self.next_song)

    def find_vc(self, guild):
        for v in self.bot.voice_clients:
            if v.guild == guild:
                return v
