from .citation import build_source_context, normalize_citations, citations_from_results
from .config import MIN_RELEVANCE


SYSTEM_RULES = """
You are an evidence-grounded research assistant.
Answer ONLY from the supplied evidence. Do not use outside knowledge.
Every factual claim must have one or more citations in the form [S1], [S2], etc.
Use only citation IDs that actually appear in the evidence.
If the evidence is insufficient, say exactly that the provided sources do not contain enough evidence to answer the question.
Do not invent authors, dates, page numbers, statistics, or references.
Prefer a concise synthesis over copying source text.
""".strip()


def make_prompt(question, results):
    context = build_source_context(results)
    return f"""{SYSTEM_RULES}\n\nQUESTION:\n{question}\n\nEVIDENCE:\n{context}\n\nWrite a concise research summary. Cite each substantive claim with [S#]."""


def answer_question(question, retriever, llm):
    results = retriever.search(question)
    if not results or results[0].score < MIN_RELEVANCE:
        return {
            "status": "insufficient_evidence",
            "question": question,
            "answer": "The provided sources do not contain enough evidence to answer this question.",
            "citations": [],
            "retrieved": [],
        }

    prompt = make_prompt(question, results)
    raw = llm.generate(prompt)
    answer = normalize_citations(raw, results)
    return {
        "status": "answered",
        "question": question,
        "answer": answer,
        "citations": citations_from_results(results),
        "retrieved": [
            {"source": r.source, "page": r.page, "score": round(r.score, 4), "text": r.text}
            for r in results
        ],
    }
