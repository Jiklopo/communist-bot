import discord
import discord.ext.commands as cmd

# Not an archive!
path = 'resources/targets.kgb'


class Surveillance(cmd.Cog):
    users = []

    def __init__(self, bot: cmd.Bot):
        self.bot = bot
        Surveillance.users = self.decode()

    @cmd.command()
    async def watch(self, ctx: cmd.Context):
        """Начать слежку за кем-то."""
        if ctx.message.mention_everyone:
            await ctx.send('Слежка за всеми невозможна.')
            return
        for m in ctx.message.mentions:
            await ctx.send(self.add(m.id))

    def add(self, user_id):
        if self.bot.user.id == user_id:
            return 'Я слежу за собой. В отличие от некоторых.'
        if user_id in Surveillance.users:
            return f'Я уже слежу за <@{user_id}>'
        with open(path, 'a') as f:
            f.write(str(user_id))
            Surveillance.users.append(user_id)
            return f'Начал слежку за <@{user_id}>'

    @staticmethod
    def decode():
        with open(path, 'r') as f:
            users = f.read().split('\n')
        return [int(u) for u in users]

    @staticmethod
    def is_watching(user_id):
        return user_id in Surveillance.users
