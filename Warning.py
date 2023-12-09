## Imports ## 
import pandas as pd
from ApiCall import *
from Location import * 
import numpy as np

## Return: String
class Warning: 
    def __init__(self):
        warnings = ApiCall.getData(self)
        warnings.replace('', np.nan, inplace=True)
        warnings = warnings[warnings['Plz'].notna()]
        warnings.to_csv('api.csv', index=True)  
    
    # Postleitzahl abfragen 
    def getPlz(self, ort):
        plzChat = Location(ort).getPostalCode()
        return plzChat
    
    # Warnings ohne Plz aus Dataframe entfernen
    def cleanWarnings(self):
        self.warnings.replace('', np.nan, inplace=True)
        warnings = self.warnings[self.warnings['Plz'].notna()]
        return warnings
    
    # Orte in Warnungen suchen
    def getWarningOrt(self, ort):
        plz2 = self.getPlz(ort)
        plz2 = plz2.iloc[0]['name']
        
        try: 
            plz2 = int(plz2)
        except: 
            fehler = "Keine Warnung gefunden"
            print("Fehler")
            return fehler

        print(type(plz2))
        print(plz2)
        
        # Datafrme mit Warnings erstellen
        data = pd.read_csv('api.csv')
        print(data)

        # Plz in DF suchen
        gesuchte_zeile = data.loc[data['Plz'] == plz2]
        print(gesuchte_zeile)
        print("zeile")
        
        # Warnung ausgeben
        if gesuchte_zeile.empty:
            print("fehler")
            fehler = "Keine Warnung gefunden"
            return fehler
        else:
            wert_als_string = gesuchte_zeile.iloc[0]
            print("in schleife")
            return wert_als_string['Titel']
        
    
## Testing Waring 

# plz = Warning("Rottach-Egern")
# gesuchte_zeile = plz.getWarningOrt()
# print(gesuchte_zeile)
