import logging
from discord.ext import commands
from src.clients.ssmClient import SecretClient
from src.cogs.help import Help
from src.cogs.data import Data
from src.cogs.checkin import Checkin
from src.cogs.deadline import WeeklyDeadline
from src.cogs.payperiod import MonthlyPayPeriod
from src.clients.ddbClient import DynamoClient

logging.basicConfig(filename="betbot.log", encoding="utf-8", level=logging.DEBUG)

ssmClient = SecretClient("us-west-2")
TOKEN = ssmClient.getSecret("prod/betbot/token")
bot = commands.Bot(command_prefix=">")

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

bot.remove_command("help")

bot.run(TOKEN)
