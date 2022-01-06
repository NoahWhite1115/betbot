from discord.ext import commands, tasks
from time_helper import strToTime, dateAsStr
import json
from datetime import datetime

class Checkin(commands.Cog):
    def __init__(self, bot, player_file, bet_file):
        self.bot = bot
        self._last_member = None
        self.player_file = player_file
        self.bet_file = bet_file

    @commands.command()
    async def checkin(self, ctx):
        #validate_message(ctx.message)

        #refactor to use context manager
        f = open(self.player_file, 'r')
        player_info = json.load(f)
        f.close()
        
        f = open(self.bet_file, 'r')
        bet_info = json.load(f)
        f.close()

        if str(ctx.author.id) not in player_info.keys():
            #todo: move these to log files
            print("No player of id: " + str(ctx.author.id))
            return

        player_info[str(ctx.author.id)]['last_checkin'] = datetime.now()
        #todo: find way to auto-get names that doesn't involve player input (on checkin deadline maybe? or lookup by id?)
        player_info[str(ctx.author.id)]['name'] = ctx.author.display_name

        f = open(self.player_file, 'w')
        json.dump(player_info, f, default=str)
        f.close()

        prev_checkin = strToTime(bet_info['prev_checkin'])
        next_checkin = strToTime(bet_info['next_checkin'])

        out = ctx.author.display_name + " has checked in for the week of " + dateAsStr(prev_checkin) + " to " + dateAsStr(next_checkin)

        await ctx.send(out)