import config as cfg
from bot.combot import CommunistBot

bot = CommunistBot(command_prefix='!')
bot.run(cfg.TOKEN)
