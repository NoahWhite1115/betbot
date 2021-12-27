from discord.ext import commands, tasks
import json

class Checkin(commands.Cog):
    def __init__(self, bot, player_file):
        self.bot = bot
        self._last_member = None
        self.player_file = player_file

    @commands.command()
    async def checkin(ctx):
        #validate_message(ctx.message)

        #refactor to use context manager
        f = open(PLAYER_FILE, 'r')
        player_info = json.load(f)
        f.close()

        if str(ctx.author.id) not in player_info.keys():
            #todo: move these to log files
            print("No player of id: " + str(ctx.author.id))
            return

        player_info[str(ctx.author.id)]['last_checkin'] = datetime.now().date()
        #todo: find way to auto-save names that doesn't involve player input (on checkin deadline maybe? or lookup by id?)
        player_info[str(ctx.author.id)]['name'] = ctx.author.display_name

        f = open(PLAYER_FILE, 'w')
        json.dump(player_info, f, default=str)
        f.close()

        out = ctx.author.display_name + " has checked in for the week of " + bet_info['prev_checkin'] + " to " + bet_info['next_checkin']

        await ctx.send(out)