from discord.ext import commands

# import logging


class Checkin(commands.Cog):
    def __init__(self, bot, ddbClient):
        self.bot = bot
        self._last_member = None
        self.ddbClient = ddbClient

    @commands.command()
    async def admin_message(self, ctx, message: str):

        adminData = self.ddbClient.getAdminData()

        adminData = filter(lambda admin: admin.id == ctx.author.id, adminData)

        for admin in adminData:
            for channelId in admin.adminOf:
                messageChannel = self.bot.get_channel(channelId)

                await messageChannel.send(message)
