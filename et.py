import pandas as pd

# Beispiel DataFrame
data = {
    'Spalte1': [10, 20, 30],
    'Spalte2': ['A', 'B', 'C']
}

df = pd.DataFrame(data)

# Inhalt einer bestimmten Zelle als String zurückgeben
zeile_index = 0
spalten_name = 'Spalte2'
zellen_inhalt = str(df.at[zeile_index, spalten_name])
print(zellen_inhalt)