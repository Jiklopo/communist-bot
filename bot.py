import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix='!')


@bot.command(pass_context=True)
async def test(ctx, arg):
    await ctx.send(arg)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)
