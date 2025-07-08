import streamlit as st
from agent import load_agent 

@st.cache_resource
def get_agent():
    """
    Loads and caches the QA agent to avoid reloading on every interaction.
    """
    return load_agent()

# --- App Configuration ---
st.set_page_config(page_title="Banking AI Assistant", layout="centered")
st.title("🏦 Banking AI Assistant")
st.markdown("I am an AI assistant powered by Google Gemini 1.5 Flash. I can answer questions based on the bank's official FAQs and procedures.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("💬 Ask your banking question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("assistant"):
        with st.spinner("🔎 Thinking..."):
            qa_chain = get_agent()
            
            result = qa_chain.invoke({"query": prompt})

            answer = result["result"]
            sources_expander = st.expander("📄 View Sources")
            with sources_expander:
                for doc in result["source_documents"]:
                    st.markdown(f"- {doc.metadata.get('source', 'Unknown file')}")
            
            st.markdown(answer)

    full_response_content = answer + "\n\n"
    sources_text = "\n\n--- Sources ---\n"
    for doc in result["source_documents"]:
        sources_text += f"- {doc.metadata.get('source', 'Unknown file')}\n"
        
    st.session_state.messages.append({"role": "assistant", "content": answer})