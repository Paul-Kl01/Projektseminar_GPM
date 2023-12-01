# Datafrme mit Warnings erstellen
import pandas as pd


data = pd.read_csv('api.csv')
print(data)

plz = 86479

gesuchte_zeile = data.loc[data['Plz'] == plz]
print(gesuchte_zeile)
print("zeile")

wert_als_string = gesuchte_zeile.iloc[0]
print(wert_als_string['Titel'])
print(wert_als_string)