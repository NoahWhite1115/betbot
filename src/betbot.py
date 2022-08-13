import os
import logging
from discord.ext import commands
from clients.ssmClient import SecretClient
from cogs.help import Help
from cogs.data import Data
from cogs.checkin import Checkin
from cogs.deadline import WeeklyDeadline
from cogs.payperiod import MonthlyPayPeriod
from clients.ddbClient import DynamoClient

logging.basicConfig(
    filename='betbot.log',
    encoding='utf-8',
    level=logging.DEBUG)

ssmClient = SecretClient('us-west-2')
TOKEN = ssmClient.getSecret("prod/betbot/token")
bot = commands.Bot(command_prefix='>')

ddbClient = DynamoClient()

# features:
#  alert users who have not checked in x days in advance?
#  admin commands? ability to restore strikes, force checkin override?
#   group voting?
# Better output messages

bot.add_cog(Help(bot))
bot.add_cog(Data(bot, ddbClient))
bot.add_cog(Checkin(bot, ddbClient))
bot.add_cog(WeeklyDeadline(bot, ddbClient))
bot.add_cog(MonthlyPayPeriod(bot, ddbClient))

bot.remove_command('help')

bot.run(TOKEN)
