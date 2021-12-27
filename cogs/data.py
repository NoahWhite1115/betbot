import discord
from discord.ext import commands, tasks
import json

class Data(commands.Cog):
    def __init__(self, bot, player_file):
        self.bot = bot
        self._last_member = None
        self.player_file = player_file

    @commands.command()
    async def bet_data(self, ctx, name: str = "all"):

        f = open(self.player_file, 'r')
        player_info = json.load(f)
        f.close()

        embedVar = discord.Embed(title="Player data:", color=0x9e7606)

        if name == "all":
            
            for player in player_info.values():
                embedVar.add_field(name= f"{player['name']} owes:" , value=str(player['owes']), inline=False)
                embedVar.add_field(name=f"{player['name']} strikes:" , value=str(player['strikes']), inline=False)
                embedVar.add_field(name=f"{player['name']} last checkin:" , value=f"{player['last_checkin']}", inline=False)
            
            #todo: show game info, like next check-in date or total pot here

        elif name == "me":
            player = ctx.player.id

            #fn for this code?
            embedVar.add_field(name= f"{player['name']} owes:" , value=str(player['owes']), inline=False)
            embedVar.add_field(name=f"{player['name']} strikes:" , value=str(player['strikes']), inline=False)
            embedVar.add_field(name=f"{player['name']} last checkin:" , value=f"{player['last_checkin']}", inline=False)

        #todo: allow searches on player username

        await ctx.send(embed = embedVar)