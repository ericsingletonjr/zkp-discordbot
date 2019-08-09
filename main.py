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
SheetCommands = SheetQuery(gClient,sheetCache)
# print("=== SHEET COMMANDS LOADED ===")
botCommands = DiscordCommands(sheetCache,SheetCommands)
print("-------")


#=== main program ===
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
        if contents[0] not in botCommands.CommandTable:
            msg = 'Looks like you\'re dumb...that command no goo'.format(message)
            await message.channel.send(msg)
        elif contents[0] in botCommands.CommandTable:
            if botCommands.CommandTable[contents[0]][1] == True and str(message.author) not in sheetCache.OfficerTable:
                msg = 'This command does exist but you are not an Officer'.format(message)
                await message.channel.send(msg)
            if len(contents) < botCommands.CommandTable[contents[0]][2] or len(contents) > botCommands.CommandTable[contents[0]][2]:
                msg = 'This is the wrong amount of arguments for that command\n'
                msg = msg + 'This command takes ' + str(botCommands.CommandTable[contents[0]][2] - 1) + ' additional arguments'
                await message.channel.send(msg.format(message))
            else:
                msg = 'Running ' + contents[0] + ' now...'.format(message)
                await message.channel.send(msg)
                botCommands.CommandTable[contents[0]][0](*contents[1:])

    '''
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    if message.content.startswith('!printshit'):
        keys = ''
        for key in SheetCommands.sheetCache.OfficerTable:
            keys = keys + ' ' + key + '\n'
        msg = 'Yeah, {0.author.mention} - I print \n' + keys + ''
        msg = msg.format(message)
        await message.channel.send(msg)
    if message.content.startswith('!secretshit'):
        msg = 'Yeah, {0.author.mention} - I print...secretly tee hee '
        print(SheetCommands.sheetCache.PlayerTable.keys())
        msg = msg.format(message)
        await message.channel.send(msg)
    if message.content.startswith("!refresh"):
        msg = 'Refreshing...'.format(message)
        #msg = 'this command broke right nao'.format(msg)
        await message.channel.send(msg)
        sheetCache.Refresh()
        
    if message.content.startswith('!tithe'):
        author = str(message.author)
        if sheetCache.OfficerTable.__contains__(author):
            msg = SheetCommands.Tithe().format(message)
            await message.channel.send(msg)
        else:
            msg = 'Nah fam, you are not allowed'.format(message)
            await message.channel.send(msg)
'''


@dClient.event
async def on_ready():
    print('Logged in as')
    print(dClient.user.name)
    print(dClient.user.id)
    print('------')
    await dClient.change_presence(activity=discord.Game(name="broken af right"))

dClient.run(token)