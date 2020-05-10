import discord
from database import database as db
import discord.ext.commands as cmd

# Not an archive!
path = 'resources/targets.kgb'


class Surveillance(cmd.Cog):
    def __init__(self, bot: cmd.Bot):
        self.bot = bot

    @cmd.command()
    async def watch(self, ctx: cmd.Context):
        """Начать слежку за кем-то."""
        if ctx.message.mention_everyone:
            await ctx.send('Слежка за всеми невозможна.')
            return
        for m in ctx.message.mentions:
            await ctx.send(self.start(ctx.message.author, m))

    @cmd.command()
    async def unwatch(self, ctx: cmd.Context):
        """Прекратить слежку за кем-то"""
        if ctx.message.mention_everyone:
            await ctx.send('Перестать следить за всеми невозможно.')
            return
        for m in ctx.message.mentions:
            await ctx.send(self.stop(ctx.message.author, m))

    def start(self, watcher, target):
        if self.bot.user == target:
            return 'Я слежу за собой. В отличие от некоторых.'
        db.add_user(watcher.id, watcher.name)
        db.add_user(target.id, target.name)
        return db.start_watching(watcher.id, target.id)

    def stop(self, watcher, target):
        if self.bot.user.id == target.id:
            return 'Всегда слежу за собой и Вам советую.'
        return db.stop_watching(watcher.id, target.id)

    @staticmethod
    def is_watching(user_id):
        return db.is_watching(user_id)
