## Imports ##
from functools import partial
from geopy.geocoders import Nominatim # Openstreatmaps 
import requests
import json
import pandas as pd 

## Return: Dataframe 
class Location: 
    # Input: Location resp. Ort, zu welchem die Plz bestimmt werden soll
    def __init__(self, location): 
        self.location = location
        self.df = self.jsonToDf()
    
    # JSON in Dataframe speichern    
    def jsonToDf(self):
        plz = pd.read_json('plz.json')
        plz["plz_name"] = plz['plz_name'].str.replace('\u00f6','Ö')
        plz["plz_name"] = plz['plz_name'].str.replace('\u00fc','ü')
        plz["plz_name"] = plz['plz_name'].str.replace('\u00df','ß')
        plz["plz_name"] = plz['plz_name'].str.replace('\u00e4','ä')
        plz["plz_name"] = plz['plz_name'].str.replace('\u00c4','Ä')
        plz["plz_name"] = plz['plz_name'].str.replace('\u00d6','Ö')
        plz["plz_name"] = plz['plz_name'].str.replace('\u00dc','Ü')
        plz["plz_name"] = plz['plz_name'].str.replace('Halle/ Saale','Halle (Saale)')
        
        mask = plz['plz_name'] == "Halle"
        plz.loc[mask, 'plz_name'] = "Halle (Weserbergland)"
        return plz
    
    # API Abfrage für Postleitzahlen     
    def getPostalJson(self):
        # Postleitzahlen per API erzahlten 
        url = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-germany-postleitzahl/exports/json?select=plz_name%2C%20name&lang=de&timezone=UTC&use_labels=false&epsg=4326'  # Ersetze dies durch die tatsächliche API-URL
        response = requests.get(url)

        # Überprüfen, ob die Anfrage erfolgreich war (Status-Code 200)
        if response.status_code == 200:
            # JSON-Antwort aus der API
            json_data = response.json()

            # Speichern der JSON-Antwort in einer Datei
            with open('plz.json', 'w') as file:
                json.dump(json_data, file)

            print('Daten erfolgreich in "api_response.json" gespeichert.')
            return json_data
        else:
            print('Fehler bei der API-Anfrage.')
    
    # Postleitzahl abfragen (in Bibliothek oder JSON Data suchen)
    def getPostalCode(self):
        try: 
            geolocator = Nominatim(user_agent="LocationApiPruefen")
            geocode = partial(geolocator.geocode, language="de")
            postleitzahl = geocode(self.location).raw.get("display_name")
            x_split = postleitzahl.split(", ")
            post_sub = x_split[4]
            columns = ['plz_name', 'name']
            df = pd.DataFrame(columns=columns)
            df.loc[0] = [self.location, post_sub]
            
            if post_sub.isdigit(): 
                return df
            else: 
                raise Exception 
        except: 
            # Dataframe PLZ durchsuchen
            gesuchter_wert = self.location
            ergebnisse = self.df[self.df['plz_name'] == gesuchter_wert]
            
            if ergebnisse.empty:
                gesuchter_wert_erw = gesuchter_wert+ " "
                ergebnisse = self.df[self.df['plz_name'].str.contains(gesuchter_wert_erw)]
                
                if ergebnisse.empty:
                   neue_zeile = pd.Series({'plz_name': "", 'name': ''})
                   ergebnisse = pd.concat([neue_zeile, ergebnisse], ignore_index=True)
                   return ergebnisse 
            return ergebnisse
            

## Testing 
#l1 = Location("Wartenberg").getPostalCode()
#print(type(l1))
