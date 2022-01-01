import discord
import json
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio

class WeeklyDeadline(commands.Cog):
    def __init__(self, bot, player_file, bet_file):
        self.index = 0
        self.bot = bot
        self.player_file = player_file
        self.bet_file = bet_file
        self.deadline.start()

    def cog_unload(self):
        self.deadline.cancel()

    @tasks.loop(hours=24*7)
    async def deadline(self):
        #use context manager
        f = open(self.bet_file, 'r')
        bet_info = json.load(f)
        f.close()

        f = open(self.player_file, 'r')
        player_info = json.load(f)
        f.close()

        #get last checkin from bet_data
        prev_checkin = datetime.strptime(bet_info['prev_checkin'], '%Y-%m-%d %H:%M:%S.%f')

        failed_players = []

        #need to check that this works
        for player in player_info.values():
            if player['active'] == False:
                pass

            player_last_checkin = datetime.strptime(player['last_checkin'], '%Y-%m-%d %H:%M:%S.%f')
            if player_last_checkin < prev_checkin:
                #todo: change this to ping
                failed_players.append(player['name'])
                player['strikes'] -= 1

                if player['strikes'] == 0:
                    player['active'] = False


        message_channel = self.bot.get_channel(bet_info['target_channel'])

        next_checkin = datetime.strptime(bet_info['next_checkin'], '%Y-%m-%d %H:%M:%S.%f')
        prev_checkin = datetime.strptime(bet_info['prev_checkin'], '%Y-%m-%d %H:%M:%S.%f')

        await message_channel.send("The week of " + str(prev_checkin.date()) + " to " + str(next_checkin.date()) + " has ended.")
        await message_channel.send("Players who lost a strike this week: " + str(failed_players))

        bet_info['prev_checkin'] = datetime.now()
        bet_info['next_checkin'] = (datetime.now() + timedelta(days=7))

        #save json data
        f = open(self.player_file, 'w')
        json.dump(player_info, f, default=str)
        f.close()

        f = open(self.bet_file, 'w')
        json.dump(bet_info, f, default=str)
        f.close()
        
        await message_channel.send("Next deadline will be " + str(bet_info['next_checkin'].date()))

    @deadline.before_loop
    async def setup_deadline(self):
        await self.bot.wait_until_ready()

        print('bot ready')

        f = open(self.bet_file, 'r')
        bet_info = json.load(f)
        f.close()

        next_checkin = datetime.strptime(bet_info['next_checkin'], '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.now()

        if (next_checkin - now).total_seconds() < 0:
            print("Next checkin time is before current time.")
            raise ValueError 

        await asyncio.sleep((next_checkin - now).total_seconds())