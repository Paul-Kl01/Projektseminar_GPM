import requests
import json
import pandas as pd
from datetime import datetime
from datetime import timezone

response = requests.get('https://nina.api.proxy.bund.dev/api31/lhp/mapData.json')

df = pd.DataFrame(columns=['Titel', 'Event', 'Datum'])
n = 0
response = response.json()

for responses in response:
    id = responses["id"]
    print(id)
    warningDetails = requests.get("https://nina.api.proxy.bund.dev/api31/warnings/"+id+".json").json() 
    meldungsText = warningDetails["info"][0]["headline"]+ ": "+warningDetails["info"][0]["description"]
    warnung = warningDetails["info"][0]["event"]
    start = warningDetails["sent"]
    d = datetime.fromisoformat(start).astimezone(timezone.utc)
    d.strftime('%Y-%m-%d %H:%M:')
    time = d.replace(tzinfo=None)
    print("- "+meldungsText)
    df.loc[n] = [meldungsText, warnung, time]
    n = n+1

print(df)

df.to_csv('file_name.csv')



