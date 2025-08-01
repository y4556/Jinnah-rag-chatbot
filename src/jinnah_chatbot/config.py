# # config.py
# import os
# from dotenv import load_dotenv,find_dotenv

# load_dotenv(find_dotenv())

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CHROMA_PATH       = os.getenv("CHROMA_PATH",    os.path.join(BASE_DIR, "chroma_db"))
# DATA_DIR          = os.getenv("DATA_DIR",       os.path.join(BASE_DIR, "data"))
# JINNAH_IMAGE_PATH = os.getenv(
#     "JINNAH_IMAGE_PATH",
#     os.path.join(BASE_DIR, "image", "Jinnah.jpg")
# )
# EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
# GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# # Processing parameters
# CHUNK_SIZE = 1000
# CHUNK_OVERLAP = 200
# RETRIEVER_K = 3
# TEMPERATURE = 0.1
# MAX_TOKENS = 4000
# src/jinnah_chatbot/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# 1) Locate your project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 2) Explicitly load the .env from the project root
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)

# 3) Now build any defaults relative to PROJECT_ROOT
CHROMA_PATH       = os.getenv("CHROMA_PATH",       str(PROJECT_ROOT / "chroma_db"))
DATA_DIR          = os.getenv("DATA_DIR",          str(PROJECT_ROOT / "data"))
JINNAH_IMAGE_PATH = os.getenv(
    "JINNAH_IMAGE_PATH",
    str(PROJECT_ROOT / "image" / "Jinnah.jpg")
)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
GROQ_MODEL      = os.getenv("GROQ_MODEL",      "llama3-70b-8192")

# Processing parameters
CHUNK_SIZE      = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP   = int(os.getenv("CHUNK_OVERLAP", 200))
RETRIEVER_K     = int(os.getenv("RETRIEVER_K", 3))
TEMPERATURE     = float(os.getenv("TEMPERATURE", 0.1))
MAX_TOKENS      = int(os.getenv("MAX_TOKENS", 4000))
