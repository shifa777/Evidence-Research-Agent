from .chunker import chunk_pages
from .config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_DIR
from .document_loader import load_pdfs
from .retriever import SemanticRetriever


def build_retriever(source_dir=DATA_DIR):
    pages = load_pdfs(source_dir)
    chunks = chunk_pages(pages, CHUNK_SIZE, CHUNK_OVERLAP)
    return SemanticRetriever(chunks), len(pages), len(chunks)
