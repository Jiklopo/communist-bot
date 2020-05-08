import os
from bot.combot import CommunistBot

bot = CommunistBot(command_prefix='!')
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
