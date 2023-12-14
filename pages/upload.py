import streamlit as st
from pathlib import Path
from pages.table import generate_files
from backend.llm import create_vectorstore_and_store
from urllib.parse import urlparse
from pdfdocument.document import PDFDocument
import requests
import re

# HEADER
st.markdown("# Dokumentenupload")
st.sidebar.markdown("# Dokumentenupload")

UPLOAD_FOLDER = './files' # Ordner für Dateiablage

# Abspeichern einer hochgeladenen Datei für die spätere Benutzung
def save_file(uploaded_file):
    save_folder = UPLOAD_FOLDER
    save_path = Path(save_folder, uploaded_file.name)
    with open(save_path, mode = 'wb') as w:
        w.write(uploaded_file.getvalue())
    if save_path.exists():
        st.success(f'Dokument {uploaded_file.name} wurde erfolgreich auf den Server hochgeladen.')

# Daten aus URL ziehen und zu PDF umwandeln
def html_url_to_pdf(html_url, output_folder = '.'):
    try:
        # HTML Content von URL holen
        response = requests.get(html_url)
        response.raise_for_status()
        html_content = response.text

        # HTML-Tags entfernen
        html_content = re.sub('<[^<]+?>', '', html_content)

        # Dateiname aus URL generieren
        parsed_url = urlparse(html_url)
        filename = parsed_url.path.split("/")[-1]
        output_pdf = f"{output_folder}/{filename}.pdf"

        # PDF erstellen
        pdf = PDFDocument(output_pdf)
        pdf.init_report()

        # HTML Content in PDF einfügen
        pdf.h3("HTML to PDF Conversion")
        pdf.p(html_content)

        # PDF speichern
        pdf.generate()

        st.success(f'Dokument {filename} wurde erfolgreich auf den Server hochgeladen.')
    except Exception as e:
        st.warning(f"Fehler beim abspeichern der pdf-Datei: {e}")
        
# PDF hochladen
with st.form('upload_form'):
    uploaded_file = st.file_uploader("Wählen Sie eine Datei aus.", type = [ ".pdf"])
    submit = st.form_submit_button(label='Hochladen')

# PDF aus URL hochladen
with st.form('link_upload_form'):
    link = st.text_input("Fügen Sie einen Link ein.")
    submit = st.form_submit_button(label='Hochladen')

# wenn submit = true URL in PDF konvertieren und hochladen & speichern
if submit:
    html_url_to_pdf(link, UPLOAD_FOLDER) 

    # Vektordatenbank generieren
    create_vectorstore_and_store()
    st.success("Vektordatenbank erfolgreich erstellt!")

# wenn submit = true PDF hochladen und abspeichern
if uploaded_file:
    filename = uploaded_file.name
    save_file(uploaded_file)

    # Vektordatenbank generieren
    create_vectorstore_and_store()
    st.success("Vektordatenbank erfolgreich erstellt!")

    # Liste neu generieren
    generate_files()
