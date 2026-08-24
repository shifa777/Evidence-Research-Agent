import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_pages(pages, chunk_size=900, overlap=150):
    """Create overlapping word chunks while retaining source/page metadata."""
    chunks = []
    for page in pages:
        words = clean_text(page["text"]).split()
        if not words:
            continue
        start = 0
        chunk_id = 0
        while start < len(words):
            end = min(len(words), start + chunk_size)
            text = " ".join(words[start:end])
            chunks.append({
                "chunk_id": f"{page['source']}::p{page['page']}::c{chunk_id}",
                "source": page["source"],
                "page": page["page"],
                "text": text,
            })
            if end == len(words):
                break
            start = max(end - overlap, start + 1)
            chunk_id += 1
    return chunks
