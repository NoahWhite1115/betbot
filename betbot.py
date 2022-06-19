import os
import logging
from dotenv import load_dotenv
from discord.ext import commands
from cogs.help import Help
from cogs.data import Data
from cogs.checkin import Checkin
from cogs.deadline import WeeklyDeadline
from clients.ddbClient import DynamoClient

load_dotenv()
logging.basicConfig(
    filename='betbot.log',
    encoding='utf-8',
    level=logging.DEBUG)
TOKEN = os.getenv('BET_DISCORD_TOKEN')
bot = commands.Bot(command_prefix='>')

ddbClient = DynamoClient()
# big todo:
# 1: time-based checks
#   -Startup handling
#   -alert loop
#   -monthly update

# features:
#  alert users who have not checked in x days in advance?
#  admin commands? ability to restore strikes, force checkin override?
#   group voting?
# Better output messages

bot.add_cog(Help(bot))
bot.add_cog(Data(bot, ddbClient))
bot.add_cog(Checkin(bot, ddbClient))
bot.add_cog(WeeklyDeadline(bot, ddbClient))

bot.remove_command('help')

bot.run(TOKEN)
