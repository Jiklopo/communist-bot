import shutil
import config as cfg
from discord.ext import commands as cmd

from bot.information import Information
from bot.surveillance import Surveillance
from bot.music import Music


class CommunistBot(cmd.Bot):
    async def on_ready(self):
        shutil.rmtree(cfg.SONGS_PATH, True)
        if cfg.MUSIC_ENABLED:
            self.add_cog(Music(self))
        if cfg.SURVEILLANCE_ENABLED:
            self.add_cog(Surveillance(self))
        if cfg.INFORMATION_ENABLED:
            self.add_cog(Information(self))
        print(f'Started as {self.user}')

    async def on_message(self, msg):
        print(f'{msg.created_at} {msg.author} {msg.content}')
        if cfg.SURVEILLANCE_ENABLED and Surveillance.is_watching(msg.author.id):
            await msg.add_reaction('\N{EYES}')
        await self.process_commands(msg)
