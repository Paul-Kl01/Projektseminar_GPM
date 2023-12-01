
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
import os
from PyPDF2 import PdfReader

###########
#pip install faiss-cpu
#pip install langchain
#pip install pypdf
#pip install InstructorEmbedding
###############

# PDF in String umwandeln
def get_pdf_text(folder_path):
    text = ""
    # Durchsuche alle Dateien im angegebenen Verzeichnis
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # Überprüfe, ob die Datei die Erweiterung ".pdf" hat
        if os.path.isfile(filepath) and filename.lower().endswith(".pdf"):
            pdf_reader = PdfReader(filepath)
            for page in pdf_reader.pages:
                text += page.extract_text()
            #text += '\n'
    return text

#Chunks erstellen
def get_text_chunks(text):
    #Arbeitsweise Textsplitter definieren
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# nur zum Anlegen des lokalen Verzeichnisses "Store" und speichern der Vektor-Datenbank
def create_vectorstore_and_store(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-base")
    # Initiate Faiss DB
    vectorstoreDB = FAISS.from_texts(texts=text_chunks,embedding=embeddings)#texts=text_chunks,
    # Verzeichnis in dem die VektorDB gespeichert werden soll
    save_directory = "Store"
    #VektorDB lokal speichern
    vectorstoreDB.save_local(save_directory)
    print(vectorstoreDB)
    return None

def main():
    folder_path = './PDFs'
    pdf_text = get_pdf_text(folder_path)
    text_chunks = get_text_chunks(pdf_text)
    create_vectorstore_and_store(text_chunks)

if __name__ == '__main__':
    main()