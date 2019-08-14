# This class will be the store of our sheet functionality. All commands relating to google
# sheet manipulation will live in here. Currently a simplified version
import gspread
import discord

# --- TODO ---
# Attendance will be a mix of a discord call and gsheets stuff
# Bot will first call discord to check raid channels to grab discord ids
# and make a list

# bank on the dkp sheet
# use guild rooster as source of truth

# --- NOTES ---
# DKP is in the L column
# Bank is on worksheet "DKP", row 2

class SheetQuery:
    def __init__(self, gClient, sheetCache):
        self.gClient = gClient
        self.sheetCache = sheetCache
        self.NewPlayerList = list()
    '''
    def __init__(self, gClient, dkpConfig):
        self.gClient = gClient
        print("=== SETTING UP GSPREAD COMMANDS ===")
        
        self.dkpConfig = dkpConfig
        self.GuildRoster = gClient.open("Deja Vu").worksheet("Master")
        self.DKP = gClient.open("Deja Vu").worksheet("DKP")
        AllSheetData = self.GuildRoster.get_all_values()
        self.BankPlayer = self.DKP.row_values(2)

        self.PlayerTable = dict()
        for lists in AllSheetData:
            self.PlayerTable.update({lists[1]: lists})
        # This removes the first entry as we don't need headers
        self.PlayerTable.pop('Name')
        print(self.BankPlayer)
        '''
    
    # Function for tithe and redistribution
    def Tithe(self):
        rowNum = 2
        pool = 0
        msg = ''
        

        for key in self.sheetCache.PlayerTable:
            if key == 'Discord ID': continue
            playerList = self.sheetCache.PlayerTable.get(key)
            dkpAmount = int(playerList[11])
            amount = int(dkpAmount*float(self.sheetCache.dkpConfig.Tithe))
            pool += amount 
            playerList[11] = str(dkpAmount-amount)
            self.sheetCache.PlayerTable.update({ key: playerList })
            rowNum += 1
        
        rowNum = 2
        msg += "Total collected: " + str(pool) + '\n'
        bankCut = int(pool*float(self.sheetCache.dkpConfig.Bankcut))
        pool -= bankCut
        self.sheetCache.BankPlayer[4] = str(int(self.sheetCache.BankPlayer[4]) + bankCut)
        
        msg += "Bank Receives: " + str(bankCut) + '\n'
        msg += "Remainder: " + str(pool) + '\n'
        receive = int(pool / 40)
        msg += "Each player will receive: " + str(receive) + '\n'

        for key in self.sheetCache.PlayerTable:
            if key == 'Discord ID': continue
            playerList = self.sheetCache.PlayerTable.get(key)
            dkpAmount = int(playerList[11])

            playerList[11] = str(dkpAmount+receive)
            self.sheetCache.PlayerTable.update({ key: playerList })
            rowNum += 1
        
        rowNum = 2
        '''
        for key in self.sheetCache.PlayerTable:
            cell_range = self.sheetCache.GuildRoster.range('A'+str(rowNum)+':AD'+str(rowNum))
            index = 0
            for item in self.sheetCache.PlayerTable.get(key):
                cell_range[index].value = item
                index += 1
            self.sheetCache.GuildRoster.update_cells(cell_range)
            rowNum += 1
        
        self.sheetCache.DKP.update_acell('E2',self.sheetCache.BankPlayer[4])
        '''
        #print(self.sheetCache.PlayerTable)
        return msg

    def AddMember(self, discordID):
        discordID = discordID.replace("\\", " ")
        if self.sheetCache.PlayerTable.get(discordID) != None:
            print("=== ENTRY EXISTS ALREADY ===")
            return None
        else:
            print("=== NOT IN SHEET - CREATING NOW ===")
            self.sheetCache.PlayerTable.update({ discordID: self.NewPlayerList})
            rowNum = len(self.sheetCache.PlayerTable)
            cell_range = self.sheetCache.GuildRoster.range('A'+str(rowNum+1)+':AD'+str(rowNum+1))
            cell_range[1].value = discordID
            self.sheetCache.GuildRoster.update_cells(cell_range)
            row_list = self.sheetCache.GuildRoster.row_values(rowNum+1)
            self.sheetCache.PlayerTable.update({ discordID: row_list})


    # Func for Aution. This will be used for item drops.
    # Will create an active auction object that will exist for
    # a period of time (or ended by officer). During that time, it will 
    # be looking for bid commands and storing values.
    def Auction(self, item):
        return None
    
    # Used to invalidate an active auction.
    # If the command is invoked but no auction object is passed
    # it will send a message saying as such
    def CancelAuction(self, auctionObject):
        print("Canceled")

    def simple(self):
        print(self.sheetCache.PlayerTable)
        


