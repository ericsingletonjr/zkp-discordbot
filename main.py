#=== import modules ===
import os
import json
from gDrive_setup import creds
from dkp_var_config import DKP_Vars
from gspread_commands import SheetQuery

import gspread
import discord

#=== client setup ===
token = os.environ.get('TOKEN')

gClient = gspread.authorize(creds)
dClient = discord.Client()

#=== object setup ===
dkp_variables = DKP_Vars(gClient)
print("--------")
print("=== DKP VARIABLES LOADED ===")
SheetCommands = SheetQuery(gClient, dkp_variables)
print("=== SHEET COMMANDS LOADED ===")
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

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    if message.content.startswith('!printshit'):
        keys = ''
        for key in SheetCommands.PlayerTable:
            keys = keys + ' ' + key + '\n'
        msg = 'Yeah, {0.author.mention} - I print \n' + keys + ''
        msg = msg.format(message)
        await message.channel.send(msg)
    if message.content.startswith('!secretshit'):
        msg = 'Yeah, {0.author.mention} - I print...secretly tee hee '
        print(SheetCommands.PlayerTable.keys())
        msg = msg.format(message)
        await message.channel.send(msg)

@dClient.event
async def on_ready():
    print('Logged in as')
    print(dClient.user.name)
    print(dClient.user.id)
    print('------')
    await dClient.change_presence(activity=discord.Game(name="broken af right"))

dClient.run(token)