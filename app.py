import streamlit as st
from rag_engine import load_base, ask_rag

# Page configuration
st.set_page_config(
    page_title="SIET_chatbot",
    layout="centered"
)

# Title
st.title("Shridevi Institute of Engineering and Technology - ChatBot")
st.caption("Ask anything about college information...")
st.caption("Created by Pavani")

# API Key
mykey = st.secrets["GROQ_API_KEY"]

# Load RAG database
@st.cache_resource
def initiate_rag():
    return load_base("01_College_Information")

index, embed_model, chunks = initiate_rag()

# Number of chunks
num_chunks = 3

# Initialize chat history
if "chat_hist" not in st.session_state:
    st.session_state.chat_hist = []

# Display previous chat messages
for qa in st.session_state.chat_hist:
    with st.chat_message(qa["role"]):
        st.write(qa["content"])

# Chat input
question = st.chat_input("Ask anything about SIET college...")

if question:

    # Store user question
    st.session_state.chat_hist.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Asking RAG for answer..."):

            answer = ask_rag(
                question,
                embed_model,
                chunks,
                index,
                api_key=mykey,
                num_chunks=num_chunks
            )

        st.write(answer)

        # Store assistant response
        st.session_state.chat_hist.append({
            "role": "assistant",
            "content": answer
        })

# Clear chat button
if st.button("Clear chat"):
    st.session_state.chat_hist = []
    st.rerun()

