# This DKP class is to store all the need variables for our
# DKP algorithm to be used in the various commands
import gspread

class DKP_Vars:
    
    def __init__(self, gClient):
        self.gClient = gClient
        print("=== SETTING UP DKP VARIABLES ===")
        DKPSheet = gClient.open("Deja Vu Backend").sheet1
        self.Tithe = DKPSheet.acell("A1").value
        self.AttendencePay = DKPSheet.acell("B1").value
        self.MinBid = DKPSheet.acell("C1").value
        self.PerPlayerAmount = DKPSheet.acell("A5").value
        self.DKPScale = DKPSheet.acell("B5").value
        self.Bankcut = DKPSheet.acell("C5").value
        self.MaxTip = DKPSheet.acell("B8").value
        self.TipLimitPerWeek = DKPSheet.acell("C8").value
        self.TrialPayout = DKPSheet.acell("A10").value