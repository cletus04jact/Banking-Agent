import os
from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
print("Environment variables loaded successfully.")
def ingest():
    loaders = []
    data_dir = "scraped_data"
    for file in os.listdir(data_dir):
        if file.endswith(".txt"):
            loaders.append(TextLoader(os.path.join(data_dir, file)))

    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("vectordb/faiss_index")

if __name__ == "__main__":
    ingest()
