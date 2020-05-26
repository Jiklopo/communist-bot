from discord import FFmpegOpusAudio
from discord.ext import commands as cmd
import youtube_dl as yt
import os


class Music(cmd.Cog):
    def __init__(self, bot: cmd.Bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': 64
            }]}
        self.ydl = yt.YoutubeDL(self.ydl_opts)

    @cmd.command()
    async def anthem(self, ctx: cmd.Context):
        """Исполнить Гимн СССР в голосовом канале, в котором вы находитесь"""
        try:
            ch = ctx.author.voice.channel
            voice = await ch.connect()
            await ctx.channel.send('Здравия желаю, товарищи!')
            voice.play(FFmpegOpusAudio('resources/anthem.opus'))
        except AttributeError as e:
            print(e)
            await ctx.channel.send('Вы не подключены к голосовому каналу!')
        except Exception as e:
            print(e)
            await ctx.channel.send('У меня не получается!')

    @cmd.command()
    async def play(self, ctx: cmd.Context, link):
        try:
            ch = ctx.author.voice.channel
            voice = await ch.connect()
            info = self.ydl.extract_info(link)
            filename = f"{info['title']}-{info['id']}.opus"
            voice.play(FFmpegOpusAudio(filename))
        except AttributeError as e:
            print(e)
            await ctx.channel.send('Вы не подключены к голосовому каналу!')
        except Exception as e:
            print(e)
            await ctx.channel.send('У меня не получается!')


if __name__ == '__main__':
    nyan = 'https://www.youtube.com/watch?v=QH2-TGUlwu4'
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'preferredquality': 192
        }]
    }
    ydl = yt.YoutubeDL(ydl_opts)
    info = ydl.extract_info(nyan)
    print(info)
