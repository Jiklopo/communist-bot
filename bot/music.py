from discord import Message, FFmpegOpusAudio
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def anthem(self, msg: Message):
        try:
            ch = msg.author.voice.channel
            voice = await ch.connect()
            await msg.channel.send('Здравия желаю, товарищи!')
            voice.play(FFmpegOpusAudio('resources/anthem.opus'))
        except AttributeError as e:
            print(e)
            await msg.channel.send('Вы не подключены к голосовому каналу!')
        except Exception as e:
            print(e)
            await msg.channel.send('У меня не получается!')
