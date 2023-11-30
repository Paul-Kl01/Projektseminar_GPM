
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

def get_conversation_chain(vectorstore):
    #llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Aufruf
load_dotenv()

folder_path = './PDFs'
#text_content = get_pdf_text(folder_path)
#print(text_content.replace('\n', ' '))
pdf_text = get_pdf_text(folder_path)
text_chunks = get_text_chunks(pdf_text)
# embeddings
embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

# Initiate Faiss DB
vectorstoreDB = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
### --> danach soll das PDF-Verzeichnis gelöscht werden, bzw. Datein verschieben, weil beim nächsten Upload 
# Verzeichnis in dem die VektorDB gespeichert werden soll
save_directory = "Store"
vectorstoreDB.save_local(save_directory)
vectorstoreDB = FAISS.load_local(save_directory)

print(get_conversation_chain(vectorstoreDB))

### Similarity-Check mit LLM
#query = "Stell"
#docs = vectorstoreDB.similarity_search_with_score(query)
#print(docs)


#### Frage und Antwort mit LLM
#retriever = vectorstoreDB.as_retriever()
#model = RetrievalQAWithSourcesChain.from_chain_type(llm=)


