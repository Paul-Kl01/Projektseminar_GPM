
from langchain.embeddings import HuggingFaceInstructEmbeddings 
from langchain.vectorstores import FAISS
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
    user_question = ################

    retriever=get_vectorstore().as_retriever()
    retrieved_docs=retriever.invoke(
    user_question
    )
    print(retrieved_docs[0].page_content)
    

if __name__ == '__main__':
    main()