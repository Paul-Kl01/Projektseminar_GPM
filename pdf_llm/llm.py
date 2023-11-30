from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
##################### Max ##########################
#pip install faiss-cpu
#pip install langchain
#pip install pypdf
#pip tiktoken
loader = DirectoryLoader("/home/max/Dokumente/5.\ Semester/Projektseminar/Projektseminar_GPM/pdf_llm/pdf", loader_cls=PyPDFLoader)
pages = loader.load_and_split()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(pages)

# embeddings
embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
# Initiate Faiss DB
vectorstoreDB = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

### Similarity-Check mit LLM
query = "Datenbank"
docs = vectorstoreDB.similarity_search(query)
print(docs)

#### Frage und Antwort mit LLM
#retriever = vectorstore
##################### Max #########################