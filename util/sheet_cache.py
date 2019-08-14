# this will be the store of all the sheet information
# On load, it will grab a copy of the information needed 
# e.g. playerbase, officers, anything we deem needed from sheets
import gspread
from util.dkp_var_config import DKP_Vars


class SheetCache:
    def __init__(self, gClient):
        self.gClient = gClient
        print("=== SETTING UP SHEET CACHE ===")
        print("------------------------------")
        self.dkpConfig = DKP_Vars(gClient)
        self.GuildRoster = gClient.open("Deja Vu").worksheet("Master")
        self.DKP = gClient.open("Deja Vu").worksheet("DKP")
        self.OfficerTab = gClient.open("Deja Vu").worksheet("Officers")
        AllSheetData = self.GuildRoster.get_all_values()
        AllOfficersData = self.OfficerTab.get_all_values()
        self.BankPlayer = self.DKP.row_values(2)

        self.PlayerTable = dict()
        self.OfficerTable = dict()

        for lists in AllOfficersData:
            self.OfficerTable.update({lists[6]: lists})
        for lists in AllSheetData:
            self.PlayerTable.update({lists[1]: lists})
        self.PlayerTable.pop('Discord ID')
        self.OfficerTable.pop('Discord ID')

    def Refresh(self):
        print("=== REFRESHING STORE VALUES FROM SHEETS ===")
        self.dkpConfig = DKP_Vars(self.gClient)
        AllSheetData = self.GuildRoster.get_all_values()
        AllOfficersData = self.OfficerTab.get_all_values()

        for lists in AllOfficersData:
            self.OfficerTable.update({lists[6]: lists})

        for lists in AllSheetData:
            self.PlayerTable.update({lists[1]: lists})

        #self.PlayerTable.pop('Discord ID')
        #self.OfficerTable.pop('Discord ID')
        #print(self.PlayerTable)
