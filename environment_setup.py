
# Here we are setting up our connection to google sheets 
# and google drive. Taking this out of the main file helps clean up the main
# app
import os
from oauth2client.service_account import ServiceAccountCredentials

# === discord token ===
token = os.getenv('TOKEN')

# === google sheets info ===
gData = {
    "type": os.getenv('type'),
    "project_id": os.getenv('project_id'),
    "private_key_id": os.getenv('private_key_id'),
    "private_key": os.getenv('private_key'),
    "client_email": os.getenv('client_email'),
    "client_id": os.getenv('client_id'),
    "auth_uri": os.getenv('auth_uri'),
    "token_uri": os.getenv('token_uri'),
    "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url'),
    "client_x509_cert_url": os.getenv('client_x509_cert_url')
}

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(gData, scope)