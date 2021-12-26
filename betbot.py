#bet bot.py
import os

import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
import json
#from dotenv import load_dotenv

#load_dotenv()
PLAYER_FILE = './player_data.json'
#TOKEN = os.getenv('BET_DISCORD_TOKEN')
client = commands.Bot(command_prefix='>')

#big todo:
#1: time-based checks
#   -Better output messages
#   -Startup handling
#   -alert loop
#2: Move 

#features:
# alert users who have not checked in x days in advance? 
#admin commands? ability to restore strikes, force checkin override? 
#   group voting?

#make sure this works
#add logging
def validate_message(message):
    if message.channel.id != 911694146526412861:
        return

    if message.author == client.user:
        return

@client.event
async def on_ready():
    print(f'{client.user} is here to manage the bet!')

@tasks.loop(minutes=1)
async def weekly_check():
    await client.wait_until_ready()

    #read bet_data json
    bet_data = {
    'start_date' : '',
    'next_checkin' : '',
    'prev_checkin' : '2021-12-23',
    'target_channel': 889033125009702936
    }

    #use context manager
    f = open(PLAYER_FILE, 'r')
    player_info = json.load(f)
    f.close()

    #get last checkin from bet_data
    last_checkin = datetime.strptime(bet_data['prev_checkin'], '%Y-%m-%d')

    failed_players = []

    for player in player_info.values():
        if player['active'] == False:
            pass

        player_last_checkin = datetime.strptime(player['last_checkin'], '%Y-%m-%d')
        if player_last_checkin < last_checkin:
            #todo: change this to ping
            failed_players.append(player['name'])
            player['strikes'] -= 1

            if player['strikes'] == 0:
                player['active'] = False


    message_channel = client.get_channel(bet_data['target_channel'])

    await message_channel.send("The week of " + bet_data['prev_checkin'] " to " + bet_data['next_checkin'] + " has ended.")
    await message_channel.send("Players who lost a strike this week: " + str(failed_players))

    #save json data


    await message_channel.send("Next checkin will be " + )




@client.command()
async def bet_help(ctx):
    #validate_message(ctx.message)

    embedVar = discord.Embed(title="Help", description="Commands and what they do", color=0x9e7606)
    embedVar.add_field(name='>checkin', value='Used to signify that a workout has been completed', inline=False)
    embedVar.add_field(name='>bet_data', value='Show data about the running bet', inline=False)

    await ctx.send(embed = embedVar)

@client.command()
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
    #todo: find way to auto-save names that doesn't involve player input (on checkin deadline maybe?)
    player_info[str(ctx.author.id)]['name'] = ctx.author.display_name

    f = open(PLAYER_FILE, 'w')
    json.dump(player_info, f, default=str)
    f.close()

    #todo: get start and end dates for week
    out = ctx.author.display_name + " has checked in for the week of " #ex: "2022-1-3 to 2022-1-10"

    await ctx.send(out)

@client.command()
async def bet_data(ctx, name: str = "all"):

    f = open(PLAYER_FILE, 'r')
    player_info = json.load(f)
    f.close()

    embedVar = discord.Embed(title="Player data:", color=0x9e7606)

    if name == "all":
        
        for player in player_info.values():
            embedVar.add_field(name= f"{player['name']} owes:" , value=str(player['owed']), inline=False)
            embedVar.add_field(name=f"{player['name']} strikes:" , value=str(player['strikes']), inline=False)
            embedVar.add_field(name=f"{player['name']} last checkin:" , value=f"{player['last_checkin']}", inline=False)
        
        #todo: show game info, like next check-in date or total pot here

    elif name == "me":
        player = ctx.player.id

        #fn for this code?
        embedVar.add_field(name= f"{player['name']} owes:" , value=str(player['owed']), inline=False)
        embedVar.add_field(name=f"{player['name']} strikes:" , value=str(player['strikes']), inline=False)
        embedVar.add_field(name=f"{player['name']} last checkin:" , value=f"{player['last_checkin']}", inline=False)

    #todo: allow searches on player username

    await ctx.send(embed = embedVar)

weekly_check.start()
client.run(TOKEN)