
# Here we are setting up our connection to google sheets 
# and google drive. Taking this out of the main file helps clean up the main
# app
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('googleapi.json', scope)