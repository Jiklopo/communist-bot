import os
import discord
from discord import Message
from discord.ext import commands
from bot.watcher import Watcher
from bot.music import Music

TOKEN = os.getenv('TOKEN')
ENV = os.getenv('ENV')
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'Started as {bot.user}')


@bot.event
async def on_message(msg: Message):
    print(f'{msg.created_at} {msg.author} {msg.content}')
    if Watcher.is_watching(msg.author.id):
       await msg.add_reaction('\N{EYES}')
    await bot.process_commands(msg)


@bot.command()
async def leave(msg: Message):
    try:
        ch = msg.author.voice.channel
    except AttributeError:
        await msg.channel.send('Вы не подключены к голосовому каналу!')
        return

    if not bot.voice_clients:
        return

    for v in bot.voice_clients:
        if v.channel == ch:
            await v.disconnect()
            await msg.channel.send('До свидания.')
            return

    await msg.channel.send('Меня нет с Вами в канале.')


def start():
    bot.add_cog(Music(bot))
    bot.add_cog(Watcher(bot))
    bot.run(TOKEN)
