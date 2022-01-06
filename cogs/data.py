from time_helper import strToTime, dateAsStr, dateTimeAsStr
import discord
from discord.ext import commands, tasks
from datetime import datetime
import json

class Data(commands.Cog):
    def __init__(self, bot, player_file, bet_file):
        self.bot = bot
        self._last_member = None
        self.player_file = player_file
        self.bet_file = bet_file

    @commands.command()
    async def player_data(self, ctx, name: str = "all"):

        f = open(self.player_file, 'r')
        player_info = json.load(f)
        f.close()

        embedVar = discord.Embed(title="Player data:", color=0x9e7606)

        if name == "all":
            
            for player in player_info.values():
                embedVar.add_field(name= f"{player['name']} owes:" , value=str(player['owes']), inline=False)
                embedVar.add_field(name=f"{player['name']} strikes:" , value=str(player['strikes']), inline=False)
                embedVar.add_field(name=f"{player['name']} last checkin:" , value=f"{dateTimeAsStr(strToTime(player['last_checkin']))}", inline=False)
            
        elif name == "me":
            player = ctx.player.id

            #fn for this code?
            embedVar.add_field(name= f"{player['name']} owes:" , value=str(player['owes']), inline=False)
            embedVar.add_field(name=f"{player['name']} strikes:" , value=str(player['strikes']), inline=False)
            embedVar.add_field(name=f"{player['name']} last checkin:" , value=f"{player['last_checkin']}", inline=False)

        #todo: allow searches on player username

        await ctx.send(embed = embedVar)

    @commands.command()
    async def bet_data(self, ctx):
        
        f = open(self.bet_file, 'r')
        bet_info = json.load(f)
        f.close()

        embedVar = discord.Embed(title="Bet data:", color=0x9e7606)
        next_checkin = strToTime(bet_info['next_checkin'])
        embedVar.add_field(name= "Next checkin:" , value=dateTimeAsStr(next_checkin), inline=False)

        await ctx.send(embed = embedVar)