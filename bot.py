import os
import discord
from discord import Message, VoiceClient
from discord.ext import commands

TOKEN = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix='!')
voice_client = VoiceClient


@bot.event
async def on_ready():
    print(f'Started as {bot.user}')


@bot.event
async def on_message(msg: Message):
    print(f'{msg.created_at} {msg.author} {msg.content}')
    if msg.author != bot.user:
        await msg.add_reaction("\N{THUMBS UP SIGN}")
    await bot.process_commands(msg)


@bot.command()
async def anthem(msg: Message):
    global voice_client
    try:
        ch = msg.author.voice.channel
        voice_client = await ch.connect()
        await msg.channel.send(content='Здравия желаю, товарищи!')
        voice_client.play(discord.FFmpegOpusAudio('anthem.opus'))
    except AttributeError as e:
        print(e)
        await msg.channel.send(content='Вы не подключены к голосовому каналу!')


@bot.command()
async def leave(msg: Message):
    global voice_client
    try:
        await voice_client.disconnect()
        del voice_client
    except:
        await msg.channel.send('Я уже свободен.')


def start():
    bot.run(TOKEN)
