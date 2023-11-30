#import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
#########FAISS ist eine DB die lokal läuft
from langchain.vectorstores import FAISS
#from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
#from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

###################################
# LLM kann ausgetauscht werden mit anderen LLM bei HuggingFaceHub 
#: Name und Repo bei Huggingface muss geändert werden
###################################

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    #embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


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
#conversation = None
def handle_userinput(user_question):
    response = conversation({'question': user_question})
    chat_history = response['chat_history']

    for i, message in enumerate(chat_history):
        if i % 2 == 0:
            #Ausgabe der Frage 
            print(message.content)
        else:
            #Ausgabe der Antwort
            print(message.content)


def main():
    load_dotenv()
    
    # 1.) Einlesen der Frage des Benutzers
    user_question = input("Wie lautet deine Frage?\n")#eingabe der Frage des Benutzers von Weboberfläche
    # 2.) Frage verarbeiten 
    handle_userinput(user_question)
    # 1.) pdf-Dokumente einlesen
    pdf_docs = #pdf-Dokumente eingeben von Weboberfläche
    # 2.) pdf-Datein auslesen und String speichern
    # get pdf text
    raw_text = get_pdf_text(pdf_docs)
    # 3.) Strings zerstückeln
    # get the text chunks
    text_chunks = get_text_chunks(raw_text)
    # 4.) zerstückelte Strings in Embeddings umwandeln mit HuggingFaceInstructEmbeddings und in Vektorstore FAISS speichern (Folge von "Tokens")
    # create vector store      
    vectorstore = get_vectorstore(text_chunks)
########################
    # create conversation chain gesprächgeschichte
    conversation = get_conversation_chain(vectorstore)
    

if __name__ == '__main__':
    main()

# Ablauf: pdf in embeddings -> in vectorstore (FAISS)-> vectorestore mit vorherigen Kontext wird dann ausgewertet von einem anderen llm