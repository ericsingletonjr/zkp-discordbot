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
        self.CommandTable.update({"!refresh": [sheetCache.Refresh, True, 1]})
        self.CommandTable.update({"!tithe" : [sheetCommands.Tithe, True, 1]})
        self.CommandTable.update({"!simple" : [sheetCommands.simple, True, 1]})
        self.CommandTable.update({"!addmember" : [sheetCommands.AddMember, True, 2]})
        #self.CommandTable.update({"!cancelauction" : [sheetCommands.CancelAuction, True, 1]})

        