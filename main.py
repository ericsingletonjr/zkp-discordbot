#=== import modules ===
import os
import json
from gDrive_setup import creds
from dkp_var_config import DKP_Vars

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

#test connection
#sheet = gClient.open('Deja Vu').sheet1
#BackendSheet = gClient.open('Deja Vu Backend')
#DKP_sheet = BackendSheet.worksheet("Variables and Formula")

#list_of_hashes = sheet.get_all_records()
#print(DKP_sheet.acell('A2').value)
#sheet.update_cell(2,3, "test from local build")
print("-------")

#=== main program ===
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