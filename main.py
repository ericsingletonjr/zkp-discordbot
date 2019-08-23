#=== import modules ===
import os
import json
from dotenv import load_dotenv
load_dotenv()
from environment_setup import creds, token
#from util.dkp_var_config import DKP_Vars
from commands.gspread_commands import SheetQuery
from commands.discord_commands import DiscordCommands
from util.sheet_cache import SheetCache
from util.switches import statusCheck

import gspread
import discord

#=== client setup ===
#token = os.getenv('TOKEN')

gClient = gspread.authorize(creds)
dClient = discord.Client()

#=== object setup ===
#dkp_variables = DKP_Vars(gClient)
#print("--------")
#print("=== DKP VARIABLES LOADED ===")
sheetCache = SheetCache(gClient)
SheetCommands = SheetQuery(gClient, dClient, sheetCache)
# print("=== SHEET COMMANDS LOADED ===")
botCommands = DiscordCommands(sheetCache,SheetCommands)
print("-------")

#=== main program ===

# TODO: Probably need a message queue as well as
# a way to divide this up more
@dClient.event
async def on_message(message):
    if message.author == dClient.user:
        return

    # Some notes about message to keep handy for now

    # message itself is the class/object
    # message.content is just pure message, no other info
    # .author is discordID

    if message.content.startswith('!'):
        contents = message.content.split()
        contents[0] = contents[0].lower()
        if contents[0] not in botCommands.CommandTable:
            msg = 'Looks like you\'re dumb...that command no goo'.format(message)
            await message.channel.send(msg)
        elif contents[0] in botCommands.CommandTable:
            if botCommands.CommandTable[contents[0]][1] == True and str(message.author) not in sheetCache.OfficerTable:
                msg = 'This command does exist but you are not an Officer'.format(message)
                await message.channel.send(msg)
            if botCommands.CommandTable[contents[0]][2] == None or len(contents) == botCommands.CommandTable[contents[0]][2] :
                msg = 'Running ' + contents[0] + ' now...'.format(message)
                await message.channel.send(msg)
                code = botCommands.CommandTable[contents[0]][0](message)
                msg = str(code) + ' : ' + statusCheck(code).format(message)
                await message.channel.send(msg.format(message))
            elif len(contents) < botCommands.CommandTable[contents[0]][2] or len(contents) > botCommands.CommandTable[contents[0]][2]:
                msg = 'This is the wrong amount of arguments for that command\n'
                msg = msg + 'This command takes ' + str(botCommands.CommandTable[contents[0]][2] - 1) + ' additional arguments'
                await message.channel.send(msg.format(message))

@dClient.event
async def on_ready():
    print('Logged in as')
    print(dClient.user.name)
    print(dClient.user.id)
    print('------')
    #guild = discord.utils.get(dClient.guilds, name='Deja Vu - Classic')
    #print(guild.voice_channels[1])
    await dClient.change_presence(activity=discord.Game(name="broken af right"))

dClient.run(token)