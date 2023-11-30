
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
import os
from PyPDF2 import PdfReader
<<<<<<< HEAD
from langchain.chains import RetrievalQAWithSourcesChain
##################### Max ##########################
#pip install faiss-cpu
#pip install langchain
#pip install pypdf
#pip tiktoken
#pip install InstructorEmbedding

#loader = DirectoryLoader("/home/max/Dokumente/5.\ Semester/Projektseminar/Projektseminar_GPM/pdf_llm/pdf", loader_cls=PyPDFLoader)
#pages = loader.load_and_split()
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#docs = text_splitter.split_documents(pages)
=======
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
>>>>>>> ed9489fc1b549be95c32030888413ec51818f39a


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

<<<<<<< HEAD
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
query = "ell"
docs = vectorstoreDB.similarity_search(query)
print(docs)

#### Frage und Antwort mit LLM
#retriever = vectorstoreDB.as_retriever()
#model = RetrievalQAWithSourcesChain.from_chain_type(llm=)
##################### Max #########################
=======
#Vektorstore erstellen
def get_vectorstore(text_chunks):
    #embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Aufruf
folder_path = './PDFs'
text_content = get_pdf_text(folder_path)
#print(text_content.replace('\n', ' '))

chunks = get_text_chunks(text_content)
#print(chunks)

#vekt = get_vectorstore(chunks)
#print(vekt)
>>>>>>> ed9489fc1b549be95c32030888413ec51818f39a
