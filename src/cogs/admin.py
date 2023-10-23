from discord.ext import commands
from discord import Member
from src.dataClasses import betData
from src.exceptions.validationExceptions import notAdminException

# import logging


class Admin(commands.Cog):
    def __init__(self, bot, ddbClient):
        self.bot = bot
        self._last_member = None
        self.ddbClient = ddbClient

    @commands.command()
    async def admin_message(self, ctx, channel: int, message: str):

        betData = self.ddbClient.getBetData(channel)

        try:
            self.validate_admin(ctx, betData)
        except notAdminException:
            return

        messageChannel = self.bot.get_channel(channel)
        await messageChannel.send(message)

    @commands.command()
    async def set_lives(self, ctx, player: Member, value: int):

        betData = self.ddbClient.getBetData(ctx.channel.id)
        playerData = self.ddbClient.getPlayerData(player.id)

        try:
            self.validate_admin(ctx, betData)
        except notAdminException:
            return

        playerData.lives = value

        self.ddbClient.updatePlayerData(ctx.channel.id, player.id, playerData)

    def validate_admin(ctx, betData: betData):
        if ctx.author.id not in betData.admins:
            ctx.send(f"You are not an admin of server ${ctx.channel.id}")
            raise notAdminException(
                f"User ${ctx.author.id} is not an admin on server ${ctx.channel.id}"
            )
