from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "sources"
OUTPUT_DIR = ROOT / "outputs"
MODEL_CACHE_DIR = ROOT / ".model_cache"

load_dotenv(ROOT / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
TOP_K = int(os.getenv("TOP_K", "6"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
MIN_RELEVANCE = float(os.getenv("MIN_RELEVANCE", "0.28"))
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
