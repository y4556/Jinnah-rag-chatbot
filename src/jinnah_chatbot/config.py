import os
from pathlib import Path
from venv import logger
from dotenv import load_dotenv, find_dotenv
import logging
# Load .env from project root
load_dotenv(find_dotenv())
# --- Environment Variables ---
DATA_DIR          = os.getenv("DATA_DIR")
EMBEDDING_MODEL   = os.getenv("EMBEDDING_MODEL")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY")
GROQ_MODEL        = os.getenv("GROQ_MODEL")
COLLECTION_NAME   = os.getenv("COLLECTION_NAME")
# (Optional) If you need integers or floats:
CHUNK_SIZE     = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP  = int(os.getenv("CHUNK_OVERLAP", "200"))
RETRIEVER_K    = int(os.getenv("RETRIEVER_K", "3"))
TEMPERATURE    = float(os.getenv("TEMPERATURE", "0.1"))
MAX_TOKENS     = int(os.getenv("MAX_TOKENS", "4000"))