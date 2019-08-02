# This class will be the store of our sheet functionality. All commands relating to google
# sheet manipulation will live in here. Currently a simplified version
import gspread
from player_bucket import PlayerBucket

# --- TODO ---
# Need tithe, payout and bank cut
# From each player, take tithe, bank then takes from that entire pool

# --- TODO ---
# Attendance will be a mix of a discord call and gsheets stuff
# Bot will first call discord to check raid channels to grab discord ids
# and make a list

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
    
    # Function for tithe and redistribution
    def Tithe(self):
        rowNum = 2
        pool = 0
        msg = ''

        for key in self.PlayerTable:
            playerList = self.PlayerTable.get(key)
            dkpAmount = int(playerList[8])
            amount = int(dkpAmount*float(self.dkpConfig.Tithe))
            pool += amount 
            playerList[8] = str(dkpAmount-amount)
            self.PlayerTable.update({ key: playerList })
            rowNum += 1
        
        rowNum = 2
        msg += "Total collected: " + str(pool) + '\n'
        bankCut = int(pool*float(self.dkpConfig.Bankcut))
        pool -= bankCut
        self.BankPlayer[4] = str(int(self.BankPlayer[4]) + bankCut)
        
        msg += "Bank Receives: " + str(bankCut) + '\n'
        msg += "Remainder: " + str(pool) + '\n'
        receive = int(pool / 40)
        msg += "Each player will receive: " + str(receive) + '\n'

        for key in self.PlayerTable:
            playerList = self.PlayerTable.get(key)
            dkpAmount = int(playerList[8])

            playerList[8] = str(dkpAmount+receive)
            self.PlayerTable.update({ key: playerList })
            rowNum += 1
        
        rowNum = 2
        
        for key in self.PlayerTable:
            cell_range = self.GuildRoster.range('A'+str(rowNum)+':W'+str(rowNum))
            index = 0
            for item in self.PlayerTable.get(key):
                if index < 23:
                    cell_range[index].value = item
                index += 1
            self.GuildRoster.update_cells(cell_range)
            rowNum += 1

        self.DKP.update_acell('E2',self.BankPlayer[4])
        
        return msg

    def Refresh(self):
        print("=== REFRESHING STORE VALUES FROM SHEETS ===")
        AllSheetData = self.GuildRoster.get_all_values()
        for lists in AllSheetData:
            self.PlayerTable.update({lists[0]: lists})
        self.PlayerTable.pop('Name')
        print("=== COMPLETED - PlayerTable is up to date ===")

        


