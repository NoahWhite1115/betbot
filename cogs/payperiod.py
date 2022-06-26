import logging
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from helpers.time_helper import strToTime
from exceptions.ddbExceptions import channelNotFoundException, \
    playerNotFoundException
import asyncio


class MonthlyPayPeriod(commands.Cog):
    def __init__(self, bot, ddbClient):
        self.bot = bot
        self.ddbClient = ddbClient
        self.payPeriod.start()

    def cog_unload(self):
        self.payPeriod.cancel()

    @tasks.loop(hours=24)
    async def payPeriod(self):
        try:
            betDataArray = self.ddbClient.getAllBetData()
        except channelNotFoundException:
            logging.error("Unable to get any bet data")
            return

        betDataArray = filter(lambda betData: strToTime(betData.nextPayPeriod) < datetime.now(), betDataArray)

        for betData in betDataArray:

            try:
                playerData = self.ddbClient.getAllPlayerData(betData.id)
            except playerNotFoundException:
                logging.error("No channel of id: " + str(betData.id))
                return

            playerData = filter(lambda player: player.active is not False, playerData)

            active_players = []

            for player in playerData:
                player.owes += betData.incrementOwes
                self.ddbClient.updatePlayerData(betData.id, player.userId, player)

                active_players.append(player.name)

            print(betData.id)

            messageChannel = self.bot.get_channel(betData.id)

            if messageChannel is None:
                logging.error("No channel of id: " + str(betData.id))
                continue

            await messageChannel.send("Amount owed for still active players has increased by " + str(betData.incrementOwes))

            betData.nextPayPeriod = datetime.now() + relativedelta(months=betData.monthsPerPayPeriod)

            self.ddbClient.updateBetData(betData.id, betData)

            await messageChannel.send("Next increment will be " + str(betData.nextPayPeriod.date()))

    @payPeriod.before_loop
    async def setupPayPeriod(self):

        await self.bot.wait_until_ready()

        now = datetime.now()
        tomorrow = now + timedelta(days=1)

        seconds = (datetime.combine(tomorrow, datetime.time.min) - now).total_seconds()

        await asyncio.sleep(seconds)
