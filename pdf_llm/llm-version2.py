
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
import os
from PyPDF2 import PdfReader
from langchain.chains import RetrievalQAWithSourcesChain
#from langchain.memory import ConversationBufferMemory
#from langchain.chains import ConversationalRetrievalChain
#from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.chat_models import ChatAnthropic
from transformers import pipeline
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


def get_vectorstore():
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-base")
    #Abruf lokaler Vektordatenbank
    save_directory = "Store"
    vectorstoreDB = FAISS.load_local(save_directory, embeddings)
    return vectorstoreDB


def main():
    load_dotenv()
    #user_question = "Wie lautet deine Frage?"
    folder_path = './PDFs'
    pdf_text = get_pdf_text(folder_path)
    text_chunks = get_text_chunks(pdf_text)
    retriever=get_vectorstore().as_retriever()
    retrieved_docs=retriever.invoke(
    "Was macht man im Katastrophenfall?"
    )
    
    #def format_docs(docs):
    #    return "\n\n".join([d.page_content for d in docs])




    #template = """Answer the question based only on the following context:

    #{context}

    #Question: {question}
    #"""
    #prompt = ChatPromptTemplate.from_template(template)
    #model = ChatAnthropic()
    #chain = (
    #{"context": retriever | format_docs, "question": RunnablePassthrough()}
    #| prompt
    #| model
    #| StrOutputParser()
    #)
    #print(chain.invoke("Was macht man im Katastrophenfall?"))
    #create_vectorstore_and_store(text_chunks)      # bei incoming pdf

    #vectorstore_DB=get_vectorstore()        # bei Abfrage durch Chatbot
    #print(get_vectorstore().similarity_search_with_score("stelle")) # zeigt an ob Vektordatenbank gefüllt ist
    
    #print(get_conversation_chain(get_vectorstore()))

    text2text_generator = pipeline("text2text-generation", model="twigs/bart-text2text-simplifier")
    print(text2text_generator(retrieved_docs[0].page_content))

if __name__ == '__main__':
    main()