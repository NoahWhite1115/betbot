import logging
from exceptions.ddbExceptions import channelNotFoundException, \
    playerNotFoundException
from helpers.time_helper import strToTime
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio


class WeeklyDeadline(commands.Cog):
    def __init__(self, bot, ddbClient):
        self.index = 0
        self.bot = bot
        self.ddbClient = ddbClient
        self.deadline.start()

    def cog_unload(self):
        self.deadline.cancel()

    @tasks.loop(hours=24)
    async def deadline(self):
        try:
            betDataArray = self.ddbClient.getAllBetData()
        except channelNotFoundException:
            logging.error("Unable to get any bet data")
            return

        betDataArray = filter(lambda betData: strToTime(betData.nextCheckin) < datetime.now(), betDataArray)

        for betData in betDataArray:

            try:
                playerData = self.ddbClient.getAllPlayerData(betData.id)
            except playerNotFoundException:
                logging.error("No channel of id: " + str(betData.id))
                return

            # get last checkin from bet_data
            prev_checkin = strToTime(betData.lastCheckin)
            next_checkin = strToTime(betData.nextCheckin)

            failed_players = []

            # need to check that this works
            for player in playerData:
                if player.active is not False:
                    playerLastCheckin = datetime.strptime(
                        player.lastCheckin,
                        '%Y-%m-%d %H:%M:%S.%f')
                    if playerLastCheckin < prev_checkin:
                        failed_players.append(player.name)
                        player.lives -= 1

                        if player.lives <= 0:
                            player.lives = 0
                            player.active = False

                self.ddbClient.updatePlayerData(betData.id, player.userId, player)

            messageChannel = self.bot.get_channel(betData.id)

            await messageChannel.send("The week of " + str(prev_checkin.date()) + " to " + str(next_checkin.date()) + " has ended.")
            await messageChannel.send("Players who lost a strike this week: " + str(failed_players))

            betData.lastCheckin = datetime.now()
            betData.nextCheckin = (datetime.now() + timedelta(days=betData.daysPerCheckinPeriod))

            self.ddbClient.updateBetData(betData.id, betData)

            await messageChannel.send("Next deadline will be " + str(betData.nextCheckin.date()))

    @deadline.before_loop
    async def setup_deadline(self):
        await self.bot.wait_until_ready()

        print('bot ready')

        '''
        now = datetime.now()
        tomorrow = now + datetime.timedelta(days=1)

        seconds = (datetime.datetime.combine(tomorrow, datetime.time.min) - now).total_seconds()

        await asyncio.sleep(seconds)
        '''
