# Datafrme mit Warnings erstellen
import pandas as pd


data = pd.read_csv('api.csv')
print(data)

plz = 86479

gesuchte_zeile = data.loc[data['Plz'] == plz]
print(gesuchte_zeile)
print("zeile")