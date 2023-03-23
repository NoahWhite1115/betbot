from discord.ext import commands

# import logging


class Admin(commands.Cog):
    def __init__(self, bot, ddbClient):
        self.bot = bot
        self._last_member = None
        self.ddbClient = ddbClient

    @commands.command()
    async def admin_message(self, ctx, channel: int, message: str):

        betData = self.ddbClient.getBetData(channel)

        if ctx.author.id not in betData.admins:
            ctx.send(f"You are not an admin of server ${channel}")
            return

        messageChannel = self.bot.get_channel(channel)
        await messageChannel.send(message)
