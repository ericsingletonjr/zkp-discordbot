# Model for auction instances

# dictionary contains -
# key = discordID of bidder
# value = list [bid amount, previousbid, main/off spec]

class AuctionBucket:
    def __init__(self, owner, item):
        self.Owner = owner
        self.Item = item
        self.ListOfBidders = dict()
        self.HighestBidder = "none"
        self.HighestAmt = 0


    

