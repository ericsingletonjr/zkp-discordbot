#=== import modules ===
import os
import json
from dotenv import load_dotenv
load_dotenv()
from gDrive_setup import creds
from dkp_var_config import DKP_Vars
from gspread_commands import SheetQuery

import gspread
import discord

#=== client setup ===
token = os.getenv('TOKEN')

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
    if message.content.startswith("!refresh"):
        msg = 'Refreshing...'.format(message)
        await message.channel.send(msg)
        SheetCommands.Refresh()
    if message.content.startswith('!tithe'):
        author = str(message.author)
        if author == 'Centproc (cp_r)#7394' or author == 'Chief Secretary Zuhayr#4713':
            msg = SheetCommands.Tithe().format(message)
            await message.channel.send(msg)
        else:
            msg = 'Looks like it'.format(message)
            await message.channel.send(msg)



@dClient.event
async def on_ready():
    print('Logged in as')
    print(dClient.user.name)
    print(dClient.user.id)
    print('------')
    await dClient.change_presence(activity=discord.Game(name="broken af right"))

dClient.run(token)