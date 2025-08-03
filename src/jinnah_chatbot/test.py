from dotenv import load_dotenv, find_dotenv
import logging
from pathlib import Path  
import os 
from PIL import Image
import chromadb
from config import JINNAH_IMAGE_PATH, CHROMA_PATH,DATA_DIR
import streamlit as st 

logger = logging.getLogger(__name__)
  
print(f"Jinnah image path is: {JINNAH_IMAGE_PATH}")
image= Image.open(JINNAH_IMAGE_PATH)
image.show()
client = chromadb.PersistentClient(path=CHROMA_PATH)
collections=client.list_collections()
for col in collections:
    print(" •", col.name) 

st.set_page_config(
    page_title="Quaid-e-Azam Chat",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Quaid-e-Azam Chat")

st.image(
    JINNAH_IMAGE_PATH,
    caption="Muhammad Ali Jinnah",
    use_container_width=True
)
client = chromadb.PersistentClient(path=CHROMA_PATH)
collections = client.list_collections()

st.subheader("Collections in ChromaDB")
for col in collections:
    st.write("•", col.name)