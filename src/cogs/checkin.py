from discord.ext import commands
from exceptions.ddbExceptions import channelNotFoundException,\
    playerNotFoundException
from exceptions.validationExceptions import attachmentNotFoundException
from helpers.time_helper import strToTime, dateAsStr
import logging
from datetime import datetime


class Checkin(commands.Cog):
    def __init__(self, bot, ddbClient):
        self.bot = bot
        self._last_member = None
        self.ddbClient = ddbClient

    @commands.command()
    async def checkin(self, ctx):
        try:
            self.validateMessage(ctx.message)
        except attachmentNotFoundException:
            await ctx.send("Your message didn't have a photo attached, and will not be counted as a valid checkin")
            return

        try:
            betData = self.ddbClient.getBetData(ctx.channel.id)
        except channelNotFoundException:
            logging.error()
            return

        try:
            playerData = self.ddbClient.getPlayerData(ctx.channel.id, ctx.author.id)
        except playerNotFoundException:
            logging.error("No player of id: " + str(ctx.author.id))
            return

        playerData.lastCheckin = datetime.now()
        # TODO: There's a much safer + saner way to do this by looking up the name by id when it's needed
        playerData.name = ctx.author.display_name

        self.ddbClient.updatePlayerData(ctx.channel.id, ctx.author.id, playerData)

        lastCheckin = strToTime(betData.lastCheckin)
        nextCheckin = strToTime(betData.nextCheckin)

        out = ctx.author.display_name + " has checked in for the week of " + \
            dateAsStr(lastCheckin) + " to " + dateAsStr(nextCheckin)

        await ctx.send(out)

    def validateMessage(self, message):
        if len(message.attachments) == 0:
            raise(attachmentNotFoundException('No attachments present'))
