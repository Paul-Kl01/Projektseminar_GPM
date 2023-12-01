
from langchain.embeddings import HuggingFaceInstructEmbeddings 
from langchain.vectorstores import FAISS

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


def get_vectorstore():
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-base")
    #Abruf lokaler Vektordatenbank
    save_directory = "Store"
    vectorstoreDB = FAISS.load_local(save_directory, embeddings)
    return vectorstoreDB


def main():
    #user_question = "Wie lautet deine Frage?"

    retriever=get_vectorstore().as_retriever()
    retrieved_docs=retriever.invoke(
    "Wie entsteht Hochwasser?"
    )
    print(retrieved_docs[0].page_content)
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

    #text2text_generator = pipeline("text2text-generation", model="twigs/bart-text2text-simplifier")
    #print(text2text_generator(retrieved_docs[0].page_content, max_length= 300))

if __name__ == '__main__':
    main()