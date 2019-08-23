# Discord Command dictionary structure


'''
Stored in a dictionary as a kvp
    

    key = command
    pos0 = actual function
    pos1 = OfficerRequired?
    pos2 = numOfArgsReq
    Class.func.__code__.co_argcount
'''

class DiscordCommands:
    def __init__(self, sheetCache, sheetCommands):
        self.CommandTable = dict()

        # Hard coding for now - will need to experiment with
        # a more clean approach in the future

        # Officer commands
        self.CommandTable.update({"!refresh": [sheetCache.Refresh, True, None]})
        self.CommandTable.update({"!tithe" : [sheetCommands.Tithe, True, None]})
        self.CommandTable.update({"!simple" : [sheetCommands.simple, True, None]})
        self.CommandTable.update({"!addmember" : [sheetCommands.AddMember, True, None]})
        self.CommandTable.update({"!editmember" : [sheetCommands.EditMember, True, 4]})
        self.CommandTable.update({"!auction" : [sheetCommands.Auction, True, None]})
        self.CommandTable.update({"!cancelauction" : [sheetCommands.CancelAuction, True, None]})

        # Err'body commands
        self.CommandTable.update({"!addself" : [sheetCommands.AddSelf, False, 3]})
        self.CommandTable.update({"!bid" : [sheetCommands.Bid, False, 2]})
        self.CommandTable.update({"!cancelbid" : [sheetCommands.CancelBid, False, None]})
        self.CommandTable.update({"!minbid" : [sheetCommands.MinBid, False, None]})