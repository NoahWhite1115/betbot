import logging
from src.exceptions.ddbExceptions import (
    channelNotFoundException,
    playerNotFoundException,
)
from src.helpers.time_helper import strToTime
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio


class WeeklyDeadline(commands.Cog):
    def __init__(self, bot, ddbClient):
        self.bot = bot
        self.ddbClient = ddbClient
        self.deadline.start()

    def cog_unload(self):
        self.deadline.cancel()

    @tasks.loop(hours=1)
    async def deadline(self):
        try:
            betDataArray = self.ddbClient.getAllBetData()
        except channelNotFoundException:
            logging.error("Unable to get any bet data")
            return

        print(betDataArray)

        betDataArray = list(
            filter(
                lambda betData: strToTime(betData.nextCheckin).replace(
                    microsecond=0, second=0
                )
                < datetime.now(),
                betDataArray,
            )
        )

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

            for player in playerData:
                if player.active is not False:
                    playerLastCheckin = strToTime(player.lastCheckin)
                    if playerLastCheckin < prev_checkin:
                        failed_players.append(player.name)
                        player.lives -= 1

                        if player.lives <= 0:
                            player.lives = 0
                            player.active = False

                self.ddbClient.updatePlayerData(betData.id, player.userId, player)

            messageChannel = self.bot.get_channel(betData.id)

            if messageChannel is None:
                logging.error("No channel of id: " + str(betData.id))
                continue

            await messageChannel.send(
                "The week of "
                + str(prev_checkin.date())
                + " to "
                + str(next_checkin.date())
                + " has ended."
            )
            await messageChannel.send(
                "Players who lost a strike this week: " + str(failed_players)
            )

            betData.lastCheckin = datetime.now()
            betData.nextCheckin = datetime.now() + timedelta(
                days=betData.daysPerCheckinPeriod
            )

            self.ddbClient.updateBetData(betData.id, betData)

            await messageChannel.send(
                "Next deadline will be " + str(betData.nextCheckin.date())
            )

    @deadline.before_loop
    async def setup_deadline(self):
        await self.bot.wait_until_ready()

        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(
            microsecond=0, second=0, minute=0
        )

        seconds = (next_hour - now).total_seconds()

        await asyncio.sleep(seconds)
