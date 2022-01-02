import sys
sys.path.append("./cogs")
sys.path.append("./helpers")

from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import os

from help import Help
from data import Data
from checkin import Checkin
from deadline import WeeklyDeadline


load_dotenv()
PLAYER_FILE = './player_data.json'
BET_FILE = './bet_data.json'
TOKEN = os.getenv('BET_DISCORD_TOKEN')
bot = commands.Bot(command_prefix='>')

#big todo:
#1: time-based checks
#   -Startup handling
#   -alert loop
#   -monthly update

#add warnings to bet info file if it changed since last checkin (to prevent cheating)

#features:
# alert users who have not checked in x days in advance? 
# admin commands? ability to restore strikes, force checkin override? 
#   group voting?
#Better output messages

bot.add_cog(Help(bot))
bot.add_cog(Data(bot, PLAYER_FILE, BET_FILE))
bot.add_cog(Checkin(bot, PLAYER_FILE, BET_FILE))
bot.add_cog(WeeklyDeadline(bot, PLAYER_FILE, BET_FILE))

bot.remove_command('help')

print(TOKEN)
bot.run(TOKEN)