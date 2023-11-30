import pandas as pd

# Beispiel DataFrame
data = {
    'Spalte1': [10, 20, 30],
    'Spalte2': [5, 15, 25]
}

df = pd.DataFrame(data)

# Berechnung der neuen Spalte und Hinzufügen zum DataFrame
df['Gesamt'] = df['Spalte1'] + df['Spalte2']

print(df)