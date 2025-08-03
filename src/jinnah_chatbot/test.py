from pathlib import Path  
import logging
import chromadb
import streamlit as st 
import os

# Initialize logger
logger = logging.getLogger(__name__)

# 1. Determine root directory (project root)
ROOT = Path(__file__).resolve().parent.parent.parent
logger.info(f"Project root: {ROOT}")

# 2. Define all paths relative to root
JINNAH_IMAGE_PATH = ROOT / "image" / "Jinnah.jpg"
CHROMA_PATH = ROOT / "chroma_db"
DATA_DIR = ROOT / "data"

# 3. Log important paths
logger.info(f"Jinnah image path: {JINNAH_IMAGE_PATH}")
logger.info(f"ChromaDB path: {CHROMA_PATH}")
logger.info(f"Data directory: {DATA_DIR}")

# 4. Verify image exists
if not JINNAH_IMAGE_PATH.exists():
    logger.error(f"Jinnah image not found at: {JINNAH_IMAGE_PATH}")
    # Fallback: Try to find any image in the directory
    image_dir = JINNAH_IMAGE_PATH.parent
    found_image = None
    if image_dir.exists():
        for file in image_dir.iterdir():
            if file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                found_image = file
                break
    if found_image:
        logger.warning(f"Using fallback image: {found_image}")
        JINNAH_IMAGE_PATH = found_image
    else:
        logger.error("No image found in image directory!")

# 5. Initialize ChromaDB
try:
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collections = client.list_collections()
    logger.info(f"Found {len(collections)} collections")
except Exception as e:
    logger.error(f"ChromaDB initialization failed: {e}")
    collections = []

# 6. Streamlit App
st.set_page_config(
    page_title="Quaid-e-Azam Chat",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Quaid-e-Azam Chat")

# Display image if available
if JINNAH_IMAGE_PATH.exists():
    st.image(
        str(JINNAH_IMAGE_PATH),  # Convert to string for Streamlit
        caption="Muhammad Ali Jinnah",
        use_container_width=True
    )
else:
    st.warning("Jinnah image not found!")

# Display collections
st.subheader("Collections in ChromaDB")
if collections:
    for col in collections:
        st.write("•", col.name)
else:
    st.error("No collections found in ChromaDB")