from src.exceptions.ddbExceptions import channelNotFoundException
from src.helpers.time_helper import strToTime, dateTimeAsStr
import discord
from discord.ext import commands
import logging


class Data(commands.Cog):
    def __init__(self, bot, ddbClient):
        self.bot = bot
        self._last_member = None
        self.ddbClient = ddbClient

    def addToEmbed(self, embedVar, playerData):
        embedVar.add_field(
            name=f"{playerData.name} owes:", value=str(playerData.owes), inline=False
        )
        embedVar.add_field(
            name=f"{playerData.name} lives:", value=str(playerData.lives), inline=False
        )
        embedVar.add_field(
            name=f"{playerData.name} last checkin:",
            value=f"{dateTimeAsStr(strToTime(playerData.lastCheckin))}",
            inline=False,
        )

    @commands.command()
    async def player_data(self, ctx, name: str = "all"):

        embedVar = discord.Embed(title="Player data:", color=0x9E7606)

        if name == "all":

            for player in self.ddbClient.getAllPlayerData(ctx.channel.id):
                self.addToEmbed(embedVar, player)

        elif name == "me":
            player = self.ddbClient.getPlayerData(ctx.channel.id, ctx.author.id)
            self.addToEmbed(embedVar, player)

        elif ctx.message.mentions != 0:
            for player in ctx.message.mentions:
                playerData = self.ddbClient.getPlayerData(ctx.channel.id, player.id)
                self.addToEmbed(embedVar, playerData)

        await ctx.send(embed=embedVar)

    @commands.command()
    async def bet_data(self, ctx):

        try:
            betData = self.ddbClient.getBetData(ctx.channel.id)
        except channelNotFoundException:
            logging.error("No id")
            return

        embedVar = discord.Embed(title="Bet data:", color=0x9E7606)
        nextCheckin = strToTime(betData.nextCheckin)
        nextPayPeriod = strToTime(betData.nextPayPeriod)
        embedVar.add_field(
            name="Next checkin:", value=dateTimeAsStr(nextCheckin), inline=False
        )
        embedVar.add_field(
            name="Next pay period:", value=dateTimeAsStr(nextPayPeriod), inline=False
        )

        await ctx.send(embed=embedVar)
