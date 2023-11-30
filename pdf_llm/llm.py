
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
import os
from PyPDF2 import PdfReader
from langchain.chains import RetrievalQAWithSourcesChain
###########
#pip install faiss-cpu
#pip install langchain
#pip install pypdf
#pip tiktoken
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


# Aufruf
folder_path = './PDFs'
#text_content = get_pdf_text(folder_path)
#print(text_content.replace('\n', ' '))
pdf_text = get_pdf_text(folder_path)
text_chunks = get_text_chunks(pdf_text)
# embeddings
embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
# Initiate Faiss DB
vectorstoreDB = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

### Similarity-Check mit LLM
#query = "ell"
#docs = vectorstoreDB.similarity_search(query)
#print(docs)


#### Frage und Antwort mit LLM
#retriever = vectorstoreDB.as_retriever()
#model = RetrievalQAWithSourcesChain.from_chain_type(llm=)


