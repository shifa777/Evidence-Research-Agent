from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL, TOP_K, MIN_RELEVANCE


@dataclass
class RetrievedChunk:
    chunk_id: str
    source: str
    page: int
    text: str
    score: float


class SemanticRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        texts = [c["text"] for c in chunks]
        self.embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        ) if texts else np.empty((0, 384))

    def search(self, query, top_k=TOP_K):
        if not self.chunks:
            return []
        query_vec = self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)[0]
        scores = self.embeddings @ query_vec
        indices = np.argsort(scores)[::-1][:top_k]
        return [
            RetrievedChunk(
                chunk_id=self.chunks[i]["chunk_id"],
                source=self.chunks[i]["source"],
                page=self.chunks[i]["page"],
                text=self.chunks[i]["text"],
                score=float(scores[i]),
            )
            for i in indices
        ]

    def has_sufficient_evidence(self, results):
        return bool(results) and results[0].score >= MIN_RELEVANCE
