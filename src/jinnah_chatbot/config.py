# import os
# from dotenv import load_dotenv

# # Load .env from project root
# load_dotenv()

# # Directly use environment variables as strings
# CHROMA_PATH = os.getenv("CHROMA_PATH")
# DATA_DIR = os.getenv("DATA_DIR")
# JINNAH_IMAGE_PATH = os.getenv("JINNAH_IMAGE_PATH")

# # Validate critical paths
# if not CHROMA_PATH:
#     raise ValueError("CHROMA_PATH environment variable is not set")
# if not DATA_DIR:
#     raise ValueError("DATA_DIR environment variable is not set")
# if not JINNAH_IMAGE_PATH:
#     raise ValueError("JINNAH_IMAGE_PATH environment variable is not set")

# print(f"[config] CHROMA_PATH → {CHROMA_PATH}")
# print(f"[config] DATA_DIR → {DATA_DIR}")
# print(f"[config] JINNAH_IMAGE_PATH → {JINNAH_IMAGE_PATH}")

# # Other settings
# EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
# GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# COLLECTION_NAME = os.getenv("COLLECTION_NAME", "jinnah-default")

# CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
# CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
# RETRIEVER_K = int(os.getenv("RETRIEVER_K", 3))
# TEMPERATURE = float(os.getenv("TEMPERATURE", 0.1))
# MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4000))
# D:\red_buffer\VS Code\Jinnah_ChatBot\src\jinnah_chatbot\config.py

# src/jinnah_chatbot/config.py

import os
from pathlib import Path
from venv import logger
from dotenv import load_dotenv, find_dotenv
import logging
# Load .env from project root
load_dotenv(find_dotenv())
# --- Environment Variables ---
CHROMA_PATH       = os.getenv("CHROMA_PATH")
DATA_DIR          = os.getenv("DATA_DIR")
EMBEDDING_MODEL   = os.getenv("EMBEDDING_MODEL")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY")
JINNAH_IMAGE_PATH = os.getenv("JINNAH_IMAGE_PATH")
GROQ_MODEL        = os.getenv("GROQ_MODEL")
COLLECTION_NAME   = os.getenv("COLLECTION_NAME")
logger.info(f"[config] CHROMA_PATH → {CHROMA_PATH}")
logger.info(f"[config] DATA_DIR → {DATA_DIR}")
logger.info(f"[config] JINNAH_IMAGE_PATH → {JINNAH_IMAGE_PATH}")
# (Optional) If you need integers or floats:
CHUNK_SIZE     = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP  = int(os.getenv("CHUNK_OVERLAP", "200"))
RETRIEVER_K    = int(os.getenv("RETRIEVER_K", "3"))
TEMPERATURE    = float(os.getenv("TEMPERATURE", "0.1"))
MAX_TOKENS     = int(os.getenv("MAX_TOKENS", "4000"))