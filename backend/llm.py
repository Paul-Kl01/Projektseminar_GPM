import streamlit as st
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
import os
from PyPDF2 import PdfReader
from transformers import pipeline
from transformers import AutoModel


#Methode: PDF in String umwandeln
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
    return text

# Methode: Textchunks erstellen (aus String)
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

# Methode: Erstellen der Vektor-Datenbank mithilfe der Embeddings + Lokal Abspeichern der Vektor-Datenbank
def create_vectorstore_and_store():
    folder_path = './files'
    pdf_text = get_pdf_text(folder_path)
    text_chunks = get_text_chunks(pdf_text)
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-base")
    #embeddings = HuggingFaceInstructEmbeddings(model_name="deutsche-telekom/bert-multi-english-german-squad2")
    # Initiate Faiss DB
    vectorstoreDB = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    # Verzeichnis in dem die Vektor-DB gespeichert werden soll
    save_directory = "Store"
    #VektorDB lokal speichern
    vectorstoreDB.save_local(save_directory)
    return None
    

# Methode: Lokale Vektor-Datenbank laden
def get_vectorstore():
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-base")
    #embeddings = HuggingFaceInstructEmbeddings(model_name="deutsche-telekom/bert-multi-english-german-squad2")
    #Abruf lokaler Vektordatenbank
    save_directory = "Store"
    vectorstoreDB = FAISS.load_local(save_directory, embeddings)
    return vectorstoreDB

# Methode: Frage des Nutzers mit Hilfe eines LLM beantworten. Als Datengrundlage dient der lokale Vektorstore
def get_llm_answer(user_question):
    # Retriever sucht passende Textausschnitte in den PDFs
    retriever=get_vectorstore().as_retriever()
    retrieved_docs=retriever.invoke(
    user_question
    )
    # Top 3 Suchergebnisse des Retrievers als Context speichern
    context=""+retrieved_docs[0].page_content+retrieved_docs[1].page_content+retrieved_docs[2].page_content
    # Context bereinigen
    context=context.replace("\n", " ")  
    context=context.replace("- ", "")

    # Erstelle die Question Answering-Pipeline für Deutsch
    qa_pipeline = pipeline("question-answering", model="deutsche-telekom/bert-multi-english-german-squad2", tokenizer="deutsche-telekom/bert-multi-english-german-squad2")

    # Frage beantworten mit Q&A Pipeline
    answer = qa_pipeline(question=user_question, context=context, max_length=200)

    # Erweiterungsmöglichkeit #
    # Frage und Basisantwort zusammenführen um einen Ausgabe im Satz mit Bezug zu erhalten
    # text2text_generator = pipeline("text2text-generation", model="google/flan-t5-xxl")
    # Test unter: https://huggingface.co/google/flan-t5-xxl?text=Formuliere+einen+neuen+Satz.+Frage%3A+Wie+sch%C3%BCtze+ich+mein+Haus+vor+Hochwasser%3F+Antwort%3A++durch+Einbau+einer+R%C3%BCckstausicherung.
    # Ausformulierte_Antwort=text2text_generator("Formuliere einen neuen Satz. Frage: "+question+ " Antwort: " + answer["answer"])
    # return Ausformulierte_Antwort
        
    return answer["answer"]
   
def main():
    st.set_page_config(
    page_title="Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
    )
    st.text("Chatbot Rene ist über Telegram erreichbar!")

if __name__ == '__main__':
    main()
