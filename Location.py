from functools import partial
from geopy.geocoders import Nominatim # Openstreatmaps 
import requests
import json
import pandas as pd 

class Location: 
    def __init__(self, location): 
        self.location = location
        
    def getDf(self):
        df = pd.read_json('plz.json')
        print(df.head())
        return df
        
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
    
    ## return Postleitzahl
    def getPostalCode(self):
        geolocator = Nominatim(user_agent="LocationApiPruefen")
        geocode = partial(geolocator.geocode, language="de")
        postleitzahl = geocode(self.location).raw.get("display_name")
        x_split = postleitzahl.split(", ")
        post_sub = x_split[4]
        print(post_sub)
        
        return post_sub

## Testing 
l1 = Location("Langenweddingen")
l1.getPostalCode()
l1.getDf()
