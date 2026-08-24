import re


def citation_label(index: int, source: str, page: int) -> str:
    return f"[S{index}: {source}, p. {page}]"


def build_source_context(results):
    blocks = []
    for i, r in enumerate(results, start=1):
        blocks.append(
            f"SOURCE S{i}\nFILE: {r.source}\nPAGE: {r.page}\n"
            f"EVIDENCE:\n{r.text}\nEND SOURCE S{i}"
        )
    return "\n\n".join(blocks)


def normalize_citations(answer: str, results):
    """Replace [S1] style references with source/page citations controlled by our metadata."""
    for i, r in enumerate(results, start=1):
        answer = answer.replace(f"[S{i}]", citation_label(i, r.source, r.page))
    return answer


def citations_from_results(results):
    return [citation_label(i, r.source, r.page) for i, r in enumerate(results, start=1)]
