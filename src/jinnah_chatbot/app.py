import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from groq import Groq
import os
import time
from persona import jinnah_prompt, refine_jinnah_response
from config import CHROMA_PATH,  EMBEDDING_MODEL, GROQ_MODEL, TEMPERATURE, MAX_TOKENS, RETRIEVER_K,GROQ_API_KEY,JINNAH_IMAGE_PATH
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
COLLECTION_NAME = "jinnah-443369fb"
# CHROMA_PATH="D:\\red_buffer\\VS Code\\Jinnah_ChatBot\\chroma_db"
# JINNAH_IMAGE_PATH="D:\\red_buffer\\VS Code\\Jinnah_ChatBot\\image\\Jinnah.jpg"
# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit setup
st.set_page_config(
    page_title="Dialogue with Quaid-e-Azam",
    page_icon="🇵🇰",
    layout="centered"
)

# Minimal styling
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #1e3a8a 0%, #0d47a1 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .message-jinnah {
        background: #f0f8ff;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        border-left: 4px solid #1e3a8a;
    }
    .message-user {
        background: #e6fffa;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0 8px auto;
        max-width: 80%;
        border-right: 4px solid #004d40;
    }
    .source-badge {
        background-color: #e3f2fd;
        color: #1e3a8a;
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 0.75rem;
        margin-top: 8px;
        display: inline-block;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("Quaid-e-Azam Chat")

    logger.info(f"jinnah path is: ", JINNAH_IMAGE_PATH)

    if os.path.exists(JINNAH_IMAGE_PATH):
        # Read the file as bytes and display
        with open(JINNAH_IMAGE_PATH, "rb") as f:
            img_bytes = f.read()
        st.image(
            img_bytes,
            width=240,
            caption="Muhammad Ali Jinnah",
            use_container_width=True,
        )
    else:
        st.warning(f"Jinnah image not found at:\n{JINNAH_IMAGE_PATH}")

    st.divider()
    st.subheader("System Status")
    # Status indicators will be updated here
    chroma_status = st.empty()
    groq_status = st.empty()
    st.divider()
    st.caption("Built with ❤️ for Pakistan")

# App header
st.markdown("<div class='header'>", unsafe_allow_html=True)
st.title("Dialogue with Quaid-e-Azam")
st.subheader("Converse with Muhammad Ali Jinnah, Founder of Pakistan")
st.markdown("</div>", unsafe_allow_html=True)

# Initialize ChromaDB
try:
    logger.info(f"[CHROMA] Connecting to ChromaDB at: {CHROMA_PATH}")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_db = Chroma(
        client=chroma_client,
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model
    )
    logger.info(f"chroma path is: ", CHROMA_PATH)
    chroma_status.success("✅ ChromaDB loaded")
    logger.info("[CHROMA] ChromaDB successfully loaded")
except Exception as e:
    chroma_status.error(f"❌ ChromaDB error: {str(e)}")
    logger.exception("[CHROMA] Failed to connect to ChromaDB:")
    st.error(f"Failed to load ChromaDB: {str(e)}")
    st.stop()

# Initialize Groq client
try:
    logger.info("[GROQ] Initializing Groq client...")
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    groq_status.success("✅ Groq connected")
    logger.info("[GROQ] Groq client connected successfully")
except Exception as e:
    groq_status.error(f"❌ Groq error: {str(e)}")
    st.error(f"Failed to initialize Groq client: {str(e)}")
    logger.exception("[GROQ] Failed to initialize Groq client:")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f'<div class="message-jinnah">{message["content"]}</div>', unsafe_allow_html=True)
            if "sources" in message and message["sources"]:
                sources_html = "".join(
                    f'<span class="source-badge">{os.path.basename(src)}</span>' 
                    for src in message["sources"]
                )
                st.markdown(f'<div style="margin-top:5px">{sources_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-user">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask Quaid-e-Azam..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="message-user">{prompt}</div>', unsafe_allow_html=True)
    
    # Generate response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        sources = []
        
        try:
            # Step 1: Retrieve relevant documents
            with st.spinner("Quaid-e-Azam is considering your question..."):
                retriever = vector_db.as_retriever(search_kwargs={"k": 3})
                relevant_docs = retriever.get_relevant_documents(prompt)
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
                sources = list(set([doc.metadata.get("source", "Unknown") for doc in relevant_docs]))
            
            # Step 2: Format the prompt using the imported persona template
            formatted_prompt = jinnah_prompt.format(context=context, question=prompt)
            
            # Step 3: Generate response with Groq streaming
            stream = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Muhammad Ali Jinnah. Respond exactly as he would, starting with 'I' and maintaining his formal, precise style."
                    },
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                top_p=1,
                stream=True,
                stop=None,
            )
            
            # Stream the response with typing effect
            assistant_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    chunk_content = chunk.choices[0].delta.content
                    assistant_response += chunk_content
                    
                    # Apply imported refinement function progressively
                    refined_chunk = refine_jinnah_response(assistant_response)
                    
                    # Display with typing effect
                    full_response = refined_chunk
                    response_placeholder.markdown(
                        f'<div class="message-jinnah">{full_response}</div>', 
                        unsafe_allow_html=True
                    )
                    time.sleep(0.03)  # Typing speed
            
            # Final refinement pass using imported function
            full_response = refine_jinnah_response(full_response)
            response_placeholder.markdown(
                f'<div class="message-jinnah">{full_response}</div>', 
                unsafe_allow_html=True
            )
            
            # Add sources if available
            if sources:
                sources_html = "".join(
                    f'<span class="source-badge">{os.path.basename(src)}</span>' 
                    for src in sources
                )
                st.markdown(f'<div style="margin-top:10px">Sources: {sources_html}</div>', unsafe_allow_html=True)
            
            # Add to session state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response,
                "sources": sources
            })
            
        except Exception as e:
            error_msg = f"Apologies, I encountered an error: {str(e)}"
            response_placeholder.markdown(
                f'<div class="message-jinnah">{error_msg}</div>', 
                unsafe_allow_html=True
            )
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_msg
            })

            # qwen/qwen3-32b