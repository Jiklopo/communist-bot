import os
import discord
from discord.ext import commands


class CommunistBot(commands.Bot):
    async def on_ready(self):
        print(f'Started as {self.user}')

    async def on_message(self, msg):
        print(f'{msg.created_at} {msg.author} {msg.content}')
