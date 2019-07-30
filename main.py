#=== IMPORT SECTION ===
import os
import json
from gDrive_setup import creds

import gspread
import discord

#=== CLIENT SETUPS ===
token = os.environ.get('TOKEN')

gClient = gspread.authorize(creds)
dClient = discord.Client()

#test connection
sheet = gClient.open('Deja Vu').sheet1
sheet2 = gClient.open('Deja Vu Backend').sheet1
list_of_hashes = sheet.get_all_records()
print(sheet.row_values(2))
#sheet.update_cell(2,3, "test from local build")
print("-------")

#=== MAIN PROGRAM ===
@dClient.event
async def on_message(message):
    if message.author == dClient.user:
        return
    
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

@dClient.event
async def on_ready():
    print('Logged in as')
    print(dClient.user.name)
    print(dClient.user.id)
    print('------')
    await dClient.change_presence(activity=discord.Game(name="broken af right"))

dClient.run(token)