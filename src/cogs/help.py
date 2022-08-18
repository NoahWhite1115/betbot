import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def bet_help(self, ctx):

        embedVar = discord.Embed(
            title="Help", description="Commands and what they do", color=0x9E7606
        )
        embedVar.add_field(
            name=">checkin",
            value="Used to signify that a workout has been completed",
            inline=False,
        )
        embedVar.add_field(
            name=">bet_data", value="Show data about the running bet", inline=False
        )
        embedVar.add_field(
            name=">player_data", value="Show data about the players", inline=False
        )

        await ctx.send(embed=embedVar)
