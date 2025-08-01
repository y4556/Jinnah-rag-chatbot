# import os
# from pathlib import Path
# from dotenv import load_dotenv

# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# env_path = PROJECT_ROOT / ".env"
# load_dotenv(env_path)
# CHROMA_PATH       = os.getenv("CHROMA_PATH",       str(PROJECT_ROOT / "chroma_db"))
# DATA_DIR          = os.getenv("DATA_DIR",          str(PROJECT_ROOT / "data"))
# JINNAH_IMAGE_PATH = os.getenv(
#     "JINNAH_IMAGE_PATH",
#     str(PROJECT_ROOT / "image" / "Jinnah.jpg")
# )
# EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
# GROQ_MODEL      = os.getenv("GROQ_MODEL",      "llama3-70b-8192")
# CHUNK_SIZE      = int(os.getenv("CHUNK_SIZE", 1000))
# CHUNK_OVERLAP   = int(os.getenv("CHUNK_OVERLAP", 200))
# RETRIEVER_K     = int(os.getenv("RETRIEVER_K", 3))
# TEMPERATURE     = float(os.getenv("TEMPERATURE", 0.1))
# MAX_TOKENS      = int(os.getenv("MAX_TOKENS", 4000))
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)

# Helper to resolve relative path
def resolve_path(env_var, default_path):
    path = os.getenv(env_var, str(default_path))
    resolved = PROJECT_ROOT / path if not Path(path).is_absolute() else Path(path)
    print(f"[config] {env_var} resolved to → {resolved}")
    return resolved

# Paths
CHROMA_PATH       = resolve_path("CHROMA_PATH", "chroma_db")
DATA_DIR          = resolve_path("DATA_DIR", "data")
JINNAH_IMAGE_PATH = resolve_path("JINNAH_IMAGE_PATH", "image/Jinnah.jpg")

# Other settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
GROQ_MODEL      = os.getenv("GROQ_MODEL", "llama3-70b-8192")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "jinnah-default")

CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
RETRIEVER_K   = int(os.getenv("RETRIEVER_K", 3))
TEMPERATURE   = float(os.getenv("TEMPERATURE", 0.1))
MAX_TOKENS    = int(os.getenv("MAX_TOKENS", 4000))
