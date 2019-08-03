# This DKP class is to store all the need variables for our
# DKP algorithm to be used in the various commands
import gspread

class DKP_Vars:
    
    def __init__(self, gClient):
        self.gClient = gClient
        print("=== SETTING UP DKP VARIABLES ===")
        DKPSheet = gClient.open("Deja Vu").worksheet("Variables")
        self.Tithe = DKPSheet.acell("B2").value
        self.AttendencePay = DKPSheet.acell("B3").value
        self.Bankcut = DKPSheet.acell("B4").value
        self.StalePenalty = DKPSheet.acell("B5").value
        self.MinBid = DKPSheet.acell("B6").value
        self.PerPlayerAmount = DKPSheet.acell("B7").value
        self.BankStartDKP = DKPSheet.acell("B8").value
        self.MaxTip = DKPSheet.acell("B9").value
        self.TipLimitPerWeek = DKPSheet.acell("B10").value
        self.TrialPayout = DKPSheet.acell("B11").value