# config.py
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_PATH       = os.getenv("CHROMA_PATH",    os.path.join(BASE_DIR, "chroma_db"))
DATA_DIR          = os.getenv("DATA_DIR",       os.path.join(BASE_DIR, "data"))
JINNAH_IMAGE_PATH = os.getenv(
    "JINNAH_IMAGE_PATH",
    os.path.join(BASE_DIR, "image", "Jinnah.jpg")
)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Processing parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 3
TEMPERATURE = 0.1
MAX_TOKENS = 4000