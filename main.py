#=== IMPORT SECTION ===
import os
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import discord

#=== CLIENT SETUPS ===
token = os.environ.get('TOKEN')

gData = {
    "type": os.environ.get('type'),
    "project_id": os.environ.get('project_id'),
    "private_key_id": os.environ.get('private_key_id'),
    "private_key": os.environ.get('private_key'),
    "client_email": os.environ.get('client_email'),
    "client_id": os.environ.get('client_id'),
    "auth_uri": os.environ.get('auth_uri'),
    "token_uri": os.environ.get('token_uri'),
    "auth_provider_x509_cert_url": os.environ.get('auth_provider_x509_cert_url'),
    "client_x509_cert_url": os.environ.get('client_x509_cert_url')
}

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(gData, scope)
gClient = gspread.authorize(creds)
dClient = discord.Client()

#test connection
sheet = gClient.open('Deja Vu').sheet1
sheet2 = gClient.open('Deja Vu Backend').sheet1
list_of_hashes = sheet.get_all_records()
print(sheet.row_values(2))
sheet.update_cell(2,3, "connected from heroku")
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