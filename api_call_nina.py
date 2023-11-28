import requests
import pandas as pd
from datetime import datetime
from datetime import timezone

## Api Variablen für NINA
api_variablen = {
    "hochwasser": "/lhp/mapData",
    "polizei": "/police/mapData",
    "wetter": "/dwd/mapData",
    "katwarn": "/katwarn/mapData",
    "mowas": "/mowas/mapData"
}

columns = ['ID', 'Urgency','Area', 'Titel', 'Event', 'Datum']

# NINA Api URLs 
ninaBaseUrl = "https://warnung.bund.de/api31"
ninaWarningsUrl = "https://nina.api.proxy.bund.dev/api31/warnings/"

# Einzelne NINA Warnings abfragen 
def get_api_warning(meldung):
  response = requests.get(ninaBaseUrl+meldung+".json")
  return response.json()

# Details zu NINA Warning abfragen 
def get_api_details(warning):
    n = 0
    response = get_api_warning(warning)
    df = pd.DataFrame(columns=columns)

    for responses in response:
        id = responses["id"]
        warningDetails = requests.get(ninaWarningsUrl+id+".json").json() 
        meldungsText = warningDetails["info"][0]["headline"]+ ": "+warningDetails["info"][0]["description"]
        warnung = warningDetails["info"][0]["event"]
        start = warningDetails["sent"]
        urgency = warningDetails["info"][0]["urgency"]
        area = warningDetails["info"][0]["area"][0]["areaDesc"]
        d = datetime.fromisoformat(start).astimezone(timezone.utc)
        d.strftime('%Y-%m-%d %H:%M:')
        time = d.replace(tzinfo=None)
        df.loc[n] = [id, urgency, area, meldungsText, warnung, time]
        n = n+1
    return df

## Dataframe to CSV 
def df_to_csv(data, filename): 
    data.to_csv(filename+'.csv') 
 
# Dataframe definieren    
df3 = pd.DataFrame(columns=columns) 

# API abfragen für alle NINA Variablen
for x in api_variablen:
    data_api = get_api_details(api_variablen[x])
    df3 = pd.concat([df3, data_api])

# API Daten in CSV speichern 
df_to_csv(df3, "Data")
print(df3)






