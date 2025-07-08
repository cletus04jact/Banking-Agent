import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


load_dotenv()
print("✅ Environment variables loaded successfully.")

def load_agent():
    """
    Initializes and returns the RetrievalQA chain (the "agent").
    """

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )


    vectordb = FAISS.load_local(
        "vectordb/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True 
    )


    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.8,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful AI banking assistant that answers customer queries using official bank FAQs and procedures.

Always use clear and formal language appropriate for financial communication.

Use the context provided to answer the question.

If you don’t know the answer, say you don’t know — do not make it up.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    # Set up the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
        chain_type_kwargs={
            "prompt": prompt_template,
            "document_variable_name": "context"
        },
        return_source_documents=True 
    )

    return qa_chain

def start_chat_session():
    """
    Starts an interactive chat session with the AI banking assistant.
    """
    print("Initializing AI Banking Assistant...")
    # Load the agent (the QA chain)
    qa_chain = load_agent()
    print("Assistant is ready. Type 'exit' or 'quit' to end the conversation.")
    print("-" * 50)

    while True:
        user_query = input("You: ")

        if user_query.lower() in ["quit", "exit", "bye"]:
            print("Banking Assistant: Thank you for chatting with us. Goodbye!")
            break

        if not user_query:
            continue
            
        print("Banking Assistant: Thinking...")

        response = qa_chain.invoke({"query": user_query})

        print(f"\nBanking Assistant: {response['result']}")
        
        print("\n--- Sources Used ---")
        if response.get("source_documents"):
            for i, doc in enumerate(response["source_documents"]):
                source_name = doc.metadata.get('source', 'Unknown source')
                print(f"[{i+1}] {source_name}")
        else:
            print("No specific sources were retrieved for this answer.")
        print("-" * 50)


# Main execution block
if __name__ == "__main__":
    start_chat_session()