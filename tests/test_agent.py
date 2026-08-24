import sys
from pathlib import Path

import numpy as np

# Add the project root to Python's import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.chunker import chunk_pages
from src.retriever import SemanticRetriever


class _FakeEmbeddingModel:
    """Deterministic stand-in for SentenceTransformer.

    The real retriever downloads the ``all-MiniLM-L6-v2`` model from
    Hugging Face the first time it runs. That makes the test suite:
      - fail with no internet access (CI runners, offline machines, sandboxes)
      - slow, since every fresh environment re-downloads ~90MB
      - non-deterministic, since it depends on an external service

    This fake keeps the test focused on the *ranking logic* in
    SemanticRetriever rather than on the embedding model itself, by
    returning fixed vectors for the known inputs used in the test below.
    """

    _VECTORS = {
        "artificial intelligence can support education and learning.": [1.0, 0.0],
        "banking systems manage financial transactions and credit risk.": [0.0, 1.0],
        "ai in education": [0.9, 0.1],
    }

    def encode(self, texts, normalize_embeddings=True, show_progress_bar=False):
        vectors = [self._VECTORS.get(t.strip().lower(), [0.5, 0.5]) for t in texts]
        arr = np.array(vectors, dtype=float)
        if normalize_embeddings:
            norms = np.linalg.norm(arr, axis=1, keepdims=True)
            norms[norms == 0] = 1
            arr = arr / norms
        return arr


def test_chunker_preserves_metadata():
    pages = [
        {
            "source": "test.pdf",
            "page": 3,
            "text": "AI supports learning. " * 100,
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=20,
        overlap=5,
    )

    assert chunks
    assert chunks[0]["source"] == "test.pdf"
    assert chunks[0]["page"] == 3
    assert chunks[0]["chunk_id"].startswith("test.pdf::p3")


def test_chunker_handles_empty_input():
    # Edge case: no pages, and a page with no extractable text. Neither
    # should raise, and both should simply contribute no chunks.
    assert chunk_pages([]) == []
    assert chunk_pages([{"source": "blank.pdf", "page": 1, "text": "   "}]) == []


def test_retriever_returns_ranked_results(monkeypatch):
    monkeypatch.setattr(
        "src.retriever.SentenceTransformer",
        lambda *args, **kwargs: _FakeEmbeddingModel(),
    )

    chunks = [
        {
            "chunk_id": "a",
            "source": "ai.pdf",
            "page": 1,
            "text": "Artificial intelligence can support education and learning.",
        },
        {
            "chunk_id": "b",
            "source": "bank.pdf",
            "page": 2,
            "text": "Banking systems manage financial transactions and credit risk.",
        },
    ]

    retriever = SemanticRetriever(chunks)

    results = retriever.search(
        "AI in education",
        top_k=2,
    )

    assert len(results) == 2
    assert results[0].score >= results[1].score
    # Not just "some ordering" - the AI chunk should actually be the top match.
    assert results[0].chunk_id == "a"


def test_retriever_with_no_chunks(monkeypatch):
    # Edge case: an empty index should never be searched against a real
    # model, and should report that it has no usable evidence.
    monkeypatch.setattr(
        "src.retriever.SentenceTransformer",
        lambda *args, **kwargs: _FakeEmbeddingModel(),
    )

    retriever = SemanticRetriever([])

    assert retriever.search("anything") == []
    assert retriever.has_sufficient_evidence(retriever.search("anything")) is False
