import json

read = json.load(open('discord_token.json', 'r'))
token = read["TOKEN"]