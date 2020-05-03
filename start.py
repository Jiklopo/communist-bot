import os
import bot

TOKEN = os.environ.get('TOKEN')
bot = bot.CommunistBot(command_prefix='!')
bot.run(TOKEN)
