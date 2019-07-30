
# Here we are setting up our connection to google sheets 
# and google drive. Taking this out of the main file helps clean up the main
# app
import os
from oauth2client.service_account import ServiceAccountCredentials

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