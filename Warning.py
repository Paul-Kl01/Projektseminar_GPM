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
        
    def getPlz(self):
        # Plz von Chat auslesen
        plzChat = Location(self.ort).getPostalCode()
        #print(plzChat)
        return plzChat
    
    def cleanWarnings(self):
        # Gibt Warnings die Plz haben aus 
        self.warnings.replace('', np.nan, inplace=True)
        warnings = self.warnings[self.warnings['Plz'].notna()]
        
        return warnings
    
    def getWarningOrt(self):
        # Plz aus Ort von Nutzer
        warning = Warning(self.ort)
        plz2 = warning.getPlz()
        
        # Plz aus DF extrahieren 
        plz2 = plz2.iloc[0]['name']
        
        # Datafrme mit Warnings erstellen
        data = warning.cleanWarnings()
        print(data)

        # Plz in DF suchen
        gesuchte_zeile = data.loc[data['Plz'] == plz2]
        
        if gesuchte_zeile.empty:
            fehler = "Es gibt keine Warnung"
            return fehler
        else:
            laenge_df = len(gesuchte_zeile)

            for index in range(laenge_df):
                if index in gesuchte_zeile.index:
                    wert_als_string = str(gesuchte_zeile.loc[index, 'Titel'])  
                    print(f"Wert in Zeile {index} als String:", wert_als_string)
            
            #titelWarning = str(gesuchte_zeile.loc[0, 'Titel'])
            
            return wert_als_string

## Testing Waring 

# plz = Warning("Rottach-Egern")
# plz2 = plz.compare()
# plz2 = plz2.iloc[0]['name']
# print(plz2)
# data = plz.cleanWarnings()
# print(data)
# gesuchte_zeile = data.loc[data['Plz'] == plz2]
# print("data:")
# print(gesuchte_zeile)

