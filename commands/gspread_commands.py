# This class will be the store of our sheet functionality. All commands relating to google
# sheet manipulation will live in here. Currently a simplified version
import gspread
import discord
from util.switches import editCheck, indexer
from models.auction_bucket import AuctionBucket
from models.attendance_bucket import AttendanceBucket

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
    def __init__(self, gClient, dClient, sheetCache):
        self.gClient = gClient
        self.dClient = dClient
        self.sheetCache = sheetCache
        self.NewPlayerList = list()
        self.AuctionInstances = dict()
        self.AttendanceInstances = dict()

        #self.Guild = discord.utils.get(dClient.guilds, name='Deja Vu - Classic')
        # Gets a list of VC in the order of the UI
        # TODO: clean up the input so unneeded channels are removed
        #print(self.Guild.voice_channels[1])



        # For now, only one auction can exist
        self.ActiveAuction = False
        self.Auctioneer = " "
    
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
        receive = int(pool / len(self.sheetCache.PlayerTable)-1)
        msg += "Each player will receive: " + str(receive) + '\n'

        for key in self.sheetCache.PlayerTable:
            if key == 'Discord ID': continue
            playerList = self.sheetCache.PlayerTable.get(key)
            dkpAmount = int(playerList[11])

            playerList[11] = str(dkpAmount+receive)
            self.sheetCache.PlayerTable.update({ key: playerList })
            rowNum += 1
        
        rowNum = 2
        
        for key in self.sheetCache.PlayerTable:
            cell_range = self.sheetCache.GuildRoster.range('A'+str(rowNum)+':AD'+str(rowNum))
            index = 0
            for item in self.sheetCache.PlayerTable.get(key):
                cell_range[index].value = item
                index += 1
            self.sheetCache.GuildRoster.update_cells(cell_range)
            rowNum += 1
        
        self.sheetCache.DKP.update_acell('E2',self.sheetCache.BankPlayer[4])
        
        #print(self.sheetCache.PlayerTable)
        #return msg

    def AddMember(self, discordObj):
    
        contents = discordObj.content.split()
        discordID = ' '.join(contents[1:])
        if '#' not in discordID:
            print("=== DOES NOT LOOK TO BE APPROPRIATE DISCORD ID ===")
            return 400
        if self.sheetCache.PlayerTable.get(discordID) != None:
            print("=== ENTRY EXISTS ALREADY ===")
            return 200
        else:
            print("=== NOT IN SHEET - CREATING NOW ===")
            self.sheetCache.PlayerTable.update({ discordID: self.NewPlayerList})
            rowNum = len(self.sheetCache.PlayerTable)
            cell_range = self.sheetCache.GuildRoster.range('A'+str(rowNum)+':AD'+str(rowNum))
            cell_range[1].value = discordID
            self.sheetCache.GuildRoster.update_cells(cell_range)
            row_list = self.sheetCache.GuildRoster.row_values(rowNum)
            self.sheetCache.PlayerTable.update({ discordID: row_list})
            return 201

    def AddSelf(self, discordObj):
            
        discordID = str(discordObj.author)
        contents =  discordObj.content.split()
        if self.sheetCache.PlayerTable.get(discordID) != None:
            print("=== ENTRY EXISTS ALREADY ===")
            return 200
        else:
            print("=== NOT IN SHEET - CREATING NOW ===")
            self.sheetCache.PlayerTable.update({ discordID: self.NewPlayerList})
            rowNum = len(self.sheetCache.PlayerTable)
            cell_range = self.sheetCache.GuildRoster.range('A'+str(rowNum)+':AD'+str(rowNum))
            cell_range[0].value = contents[1]
            cell_range[1].value = discordID
            cell_range[5].value = contents[2]
            self.sheetCache.GuildRoster.update_cells(cell_range)
            row_list = self.sheetCache.GuildRoster.row_values(rowNum)
            self.sheetCache.PlayerTable.update({ discordID: row_list})
            return 201

    def EditMember(self, discordObj):
        contents = discordObj.content.split()
        column = editCheck(contents[1])
        if column == 400:
            print("=== NOT A VALID PARAMETER ===")
            return column
        position = indexer(column)
        newValue = contents[2]
        discordID = contents[3].replace('/', ' ')

        if '#' not in discordID:
            print("=== DOES NOT LOOK TO BE APPROPRIATE DISCORD ID ===")
            return 400
        elif discordID not in self.sheetCache.PlayerTable:
            print("=== PLAYER NOT IN SHEET ===")
            return 404
        
        keyList = list(self.sheetCache.PlayerTable)
        rowNum = keyList.index(discordID)
        playerInfo = self.sheetCache.PlayerTable.get(discordID)
        playerInfo[position] = newValue
        self.sheetCache.PlayerTable.update({discordID: playerInfo})
        cell_range = self.sheetCache.GuildRoster.range('A'+str(rowNum+1)+':AD'+str(rowNum+1))
        cell_range[position].value = newValue
        self.sheetCache.GuildRoster.update_cells(cell_range)
        return 201

    # TODO: Will need better error handling
    def Auction(self, discordObj):

        if self.ActiveAuction:
            print("=== ACTIVE AUCTION ALREADY ===")
            return 404
        else:
            self.ActiveAuction = True

        owner = str(discordObj.author)
        self.Auctioneer = owner
        item = discordObj.content.split()
        item = ' '.join(item[1:])
        if not item:
            print("=== NO ITEM GIVEN ===")
            return 400

        instance = AuctionBucket(owner,item)
        self.AuctionInstances.update({owner: instance})
        print("=== AUCTION INSTANCE CREATED ===")
        print(owner, item, self.AuctionInstances.get(owner).Owner)
        print("================================")
        return 201
    
    def CancelAuction(self, discordObj):
        owner = str(discordObj.author)
        if owner not in self.AuctionInstances:
            print("=== NO AUCTION EXISTS ===")
            return 404
        print(owner, self.AuctionInstances.get(owner).Item)
        self.AuctionInstances.pop(owner)
        print("=== AUCTION CANCELED ===")
        self.ActiveAuction = False
        return 201

    def Bid(self, discordObj):
        if not self.ActiveAuction:
            print("=== NO ACTIVE AUCTION ===")
            return 404
        bidder = str(discordObj.author)
        amount = 0
        try:
            amount = int(' '.join(discordObj.content.split()[1:]))
        except:
            print("=== NOT A CORRECT VALUE ===")
            return 400
        if amount < int(self.sheetCache.dkpConfig.MinBid):
            print("=== DOES NOT MEET MINBID REQUIREMENTS ===")
            return 400
        '''
        if bidder in self.AuctionInstances:
            print("=== AUCTION OFFICIAL CANNOT BID ===")
            return 400
        '''
        auction = self.AuctionInstances.get(self.Auctioneer)
        if bidder not in auction.ListOfBidders:
            print("=== BIDDER DOES NOT EXIST FOR THIS AUCTION ===")
            portfolio = [amount, 0, 0]
            print(bidder, portfolio)
            auction.ListOfBidders.update({bidder: portfolio})
            print("=== ADDED BIDDER PORTFOLIO ===")

            if amount > auction.HighestAmt:
                auction.HighestAmt = amount
                auction.HighestBidder = bidder
            print(bidder, amount, auction.HighestBidder, auction.HighestAmt)
            return 201

        portfolio = auction.ListOfBidders.get(bidder)

        if amount < portfolio[0]:
            print("=== DOES NOT GO HIGHER THAN PREVIOUS BID ===")
            return 400
        portfolio[1] = portfolio[0]
        portfolio[0] = amount
        print(portfolio)
        auction.ListOfBidders.update({bidder: portfolio})

        if amount > auction.HighestAmt:
            auction.HighestAmt = amount
            auction.HighestBidder = bidder
            print(bidder, amount, auction.HighestBidder, auction.HighestAmt)
        return 200

    def MinBid(self, discordObj):
        if not self.ActiveAuction:
            print("=== NO ACTIVE AUCTION ===")
            return 404
        bidder = str(discordObj.author)
        amount = int(self.sheetCache.dkpConfig.MinBid)
        '''
        if bidder in self.AuctionInstances:
            print("=== AUCTION OFFICIAL CANNOT BID ===")
            return 400
        '''
        auction = self.AuctionInstances.get(self.Auctioneer)
        if bidder in auction.ListOfBidders:
            print("=== BIDDER EXISTS ALREADY ===")
            return 400
        
        print("=== BIDDER DOES NOT EXIST FOR THIS AUCTION ===")
        portfolio = [amount, 0, 0]
        print(bidder, portfolio)
        auction.ListOfBidders.update({bidder: portfolio})
        print("=== ADDED BIDDER PORTFOLIO ===")           
        return 201

    def CancelBid(self, discordObj):
        if not self.ActiveAuction:
            print("=== NO ACTIVE AUCTION ===")
            return 404
        bidder = str(discordObj.author)
        auction = self.AuctionInstances.get(self.Auctioneer)
        if bidder not in auction.ListOfBidders:
            print("=== THIS BIDDER DOESNOT EXIST ===")
            return 404
        auction.ListOfBidders.pop(bidder)
        print("=== REMOVED BIDDER AND CANCELLED PORTFOLIO ===")
        return 200

    # TODO: Ends auction, dkp taken from winner, divide by 40
    # bank gets leftovers 
    # (e.g. 100 = 2 (2.5) per player (80 total), 20 goes to bank)
    # (e.g. 250 = 6 (6.25) per player (240 total), 10 goes to bank)
    def EndAuction(self, discordObj):
        return None

    # TODO: attendance to check selected discord channels
    def Attendance(self, discordObj):
        return None


    # === DEBUG FUNCS FOR LOGS ===
    def simple(self, discordObj):
        #print(self.sheetCache.PlayerTable)
        #print(self.dClient.VoiceChannel)
        return 200
        

