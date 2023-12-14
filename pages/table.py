import streamlit as st
from datetime import datetime
import pandas as pd
from pathlib import Path
import os
from backend.llm import create_vectorstore_and_store


st.set_page_config(
    page_title="Hochgeladene Dokumente",
    layout="wide",
    initial_sidebar_state="expanded",
)

# HEADER
st.markdown("# Hochgeladene Dokumente")
st.sidebar.markdown("# Hochgeladene Dokumente")

field_names = ['Index', 'Titel', 'Hochladezeitpunkt']

FILES = []

# Index festelegen
def newIndex():
    lastIndex = len(FILES)
    newIndex = lastIndex + 1
    return newIndex

# alle Dateien des Ordners "files" in eine Liste schreiben
def generate_files():
    folder = './files'
    files = os.listdir(folder)
    for file in files:
        file_path = Path(folder, file)
        
        # Titel und Index zu einer Datei hinzufügen
        index = newIndex()
        title = file
        
        # Zeitstempel zu einer Datei hinzufügen -> ctime = letzte Änderung der Metadaten der Datei
        upload_time = os.path.getctime(Path(folder, file))
        upload_time = datetime.fromtimestamp(upload_time).strftime("%d.%m.%Y - %H:%M:%S")
        if os.path.isfile(file_path) and title.endswith(".pdf"):
            file_info = {
                "Index": index,
                "Titel": title,
                "Hochladezeitpunkt": upload_time
            }
            # Eintrag an Liste anhängen
            FILES.append(file_info)
    return FILES

#Löschfunktion
def delete_row_and_file(index):
    folder = './files'
    file_name = FILES[index]['Titel']
    file_path = Path(folder, file_name)

    # Datei aus "files" Ordner löschen
    try:
        os.remove(file_path)
        st.success("Datei erfolgreich gelöscht.")
    except FileNotFoundError:
        st.warning("Datei nicht gefunden.")

    # Eintrag aus Liste löschen
    FILES.pop(index)
    create_vectorstore_and_store()

# Funktion zur Darstellung der Tabelle
def display_table():
        hide_table_row_index = """ 
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
        # Tabellen-Styling Workaround durch CSS-Injection
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        # Tabelle mit aus Dataframe darstellen
        table1 = pd.DataFrame.from_dict(generate_files())
        table = st.table(table1)
        return table1

    
# Darstellung der Tabelle
col1, col2 = st.columns([0.7, 0.3])
with col1:
    display_table()

# Hinzufügen der Lösch-Buttons
with col2:
    for index in range(len(FILES)):
        delete_button = st.button("Löschen", key = index)
        if delete_button:
            delete_row_and_file(index)


