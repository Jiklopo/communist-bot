import os
from discord.ext import commands as cmd
from bot.surveillance import Surveillance
from bot.music import Music

ENV = os.getenv('ENV')


class CommunistBot(cmd.Bot):
    async def on_ready(self):
        self.add_cog(Music(self))
        self.add_cog(Surveillance(self))
        print(f'Started as {self.user}')

    async def on_message(self, msg):
        print(f'{msg.created_at} {msg.author} {msg.content}')
        if Surveillance.is_watching(msg.author.id):
            await msg.add_reaction('\N{EYES}')
        await self.process_commands(msg)

    @cmd.command()
    async def leave(self, msg):
        """Покинуть голосовой канал."""
        try:
            ch = msg.author.voice.channel
        except AttributeError:
            await msg.channel.send('Вы не подключены к голосовому каналу!')
            return

        if not self.voice_clients:
            return

        for v in self.voice_clients:
            if v.channel == ch:
                await v.disconnect()
                await msg.channel.send('До свидания.')
                return

        await msg.channel.send('Меня нет с Вами в канале.')