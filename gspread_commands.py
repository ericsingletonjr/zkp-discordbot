# This class will be the store of our sheet functionality. All commands relating to google
# sheet manipulation will live in here. Currently a simplified version
import gspread
from player_bucket import PlayerBucket

# --- TODO ---
# Need tithe, payout and bank cut
# From each player, take tithe, bank then takes from that entire pool
# then attendance is 33% of the remaining pool

# bank on the dkp sheet
# use guild rooster as source of truth

# --- NOTES ---
# DKP is in the I column
# Bank is on worksheet "DKP", row 2

class SheetQuery:
    def __init__(self, gClient, dkpConfig):
        self.gClient = gClient
        print("=== SETTING UP GSPREAD COMMANDS ===")
        self.dkpConfig = dkpConfig
        self.GuildRoster = gClient.open("Deja Vu").get_worksheet(1)
        self.DKP = gClient.open("Deja Vu").get_worksheet(2)
        AllSheetData = self.GuildRoster.get_all_values()
        self.BankPlayer = self.DKP.row_values(2)

        self.PlayerTable = dict()
        for lists in AllSheetData:
            self.PlayerTable.update({lists[0]: lists})
        # This removes the first entry as we don't need headers (for now may change)
        self.PlayerTable.pop('Name')
        print(self.BankPlayer)

        


