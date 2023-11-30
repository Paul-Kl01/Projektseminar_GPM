import pandas as pd
from ApiCall import *
from Location import * 
import numpy as np

class Warning: 
    def __init__(self, ort):
        # Ort aus Bot Anfrage 
        self.ort = ort
        # Warnings DataFrame
        self.warnings = ApiCall.getData(self)
        
    def compare(self):
        # Plz von Chat auslesen
        plzChat = Location(self.ort).getPostalCode()
        #print(plzChat)
        return plzChat
    
    def cleanWarnings(self):
        # Gibt Warnings die Plz haben aus 
        self.warnings.replace('', np.nan, inplace=True)
        warnings = self.warnings[self.warnings['Plz'].notna()]
        
        return warnings

# plz = Warning("Rottach-Egern")
# plz2 = plz.compare()

# plz2 = plz2.iloc[0]['name']
# print(plz2)

# data = plz.cleanWarnings()
# print(data)

# gesuchte_zeile = data.loc[data['Plz'] == plz2]

# print("data:")
# print(gesuchte_zeile)

