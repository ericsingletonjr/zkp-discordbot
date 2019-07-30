
# This serves to be a node or player bucket which will hold the data
# from each row. These buckets will get stored into a dictionary in the
# gspread commands as our "store" to keep track of sheet information

class PlayerBucket:
    def __init__(self, playerData):
        self.playerData = playerData