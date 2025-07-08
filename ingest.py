import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
print("✅ Environment variables loaded successfully.")

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

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    # Build and save FAISS vectorstore
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("vectordb/faiss_index")
    print("✅ Vectorstore saved successfully with embeddings.")

if __name__ == "__main__":
    ingest()
