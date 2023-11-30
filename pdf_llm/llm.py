
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
import os
from PyPDF2 import PdfReader
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
#from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv
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

def get_vectorstore_and_store(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    # Initiate Faiss DB
    ##########################vectorstoreDB = FAISS.from_texts(texts=text_chunks, embedding=embeddings)##############
    ###
    ### --> danach soll das PDF-Verzeichnis gelöscht werden, bzw. Datein verschieben, weil beim nächsten Upload 
    ###
    # Verzeichnis in dem die VektorDB gespeichert werden soll
    save_directory = "Store"
    vectorstoreDB.save_local(save_directory)
    vectorstoreDB = FAISS.load_local(save_directory, embeddings)
    return vectorstoreDB

########

def get_conversation_chain(vectorstore):
    #llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    memory.save_context({"input": "hi"}, {"output": "whats up"})
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = conversation({'question': user_question})
    chat_history = response['chat_history']



def main():
    load_dotenv()
    user_question = "Wie lautet deine Frage?"
    folder_path = './PDFs'
    pdf_text = get_pdf_text(folder_path)
    text_chunks = get_text_chunks(pdf_text)
    vectorstoreDB = get_vectorstore_and_store(text_chunks)
    #save_directory = "Store"
    #vectorstoreDB = FAISS.load_local(save_directory, embeddings)

    print(get_conversation_chain(vectorstoreDB))




if __name__ == '__main__':
    main()