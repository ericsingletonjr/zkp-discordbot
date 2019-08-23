# This stores our switch statements to help with
# ensuring that specific commands are paramaterize

# Messages to return for feedback
# TODO: Need to be more user meaningful in the future
def statusCheck(code):
    switch = {
        200: "Command was completed but nothing happend",
        201: "Command completed successfully",
        400: "Something went wrong, ensure you are using the correct syntax",
        404: "This value/request doesn't seem to exist"
    }
    return switch.get(code)

# Used to put all the columns in an easier format
# for editing the main sheet

# TODO: Makes sense to update it to columns grabbed from cache so
# update it to be more dynamic in the future
def editCheck(arg):
    switch = {
        'name': 'A',
        'discordID': 'B',
        'altDiscord': 'C',
        'bnet': 'D',
        'altBnet': 'E',
        'main': 'F',
        'class': 'G',
        'race': 'H',
        'role': 'I',
        'rank': 'J',
        'status': 'K',
        'DKP': 'L',
        'duelElo': 'M',
        'prof1': 'N',
        'prof2': 'O',
        'joined': 'P',
        'timezone': 'Q',
        'alt1': 'R',
        'alt1Class': 'S',
        'alt1Role': 'T',
        'alt2': 'U',
        'alt2Class': 'V',
        'alt2Role': 'W',
        'alt3': 'X',
        'alt3Class': 'Y',
        'alt3Role': 'Z',
        'attendPercent': 'AA',
        'totalTipped': 'AB',
        'totalDKPrec': 'AC',
        'miscNotes': 'AD'
    }
    return switch.get(arg, 400)

# Used to grab index of values in our sheet
# for editing purposes
def indexer(arg):
    switch = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7,
        'I ': 8,
        'J': 9,
        'K': 10,
        'L': 11,
        'M': 12,
        'N': 13,
        'O': 14,
        'P': 15,
        'Q': 16,
        'R': 17,
        'S': 18,
        'T': 19,
        'U': 20,
        'V': 21,
        'W': 22,
        'X': 23,
        'Y': 24,
        'Z': 25,
        'AA': 26,
        'AB': 27,
        'AC': 28,
        'AD': 29
    }
    return switch.get(arg)