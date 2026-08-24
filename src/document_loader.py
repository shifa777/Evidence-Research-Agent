from pathlib import Path
from pypdf import PdfReader


def load_pdfs(source_dir: Path):
    """Read every PDF and preserve page-level metadata for citations."""
    documents = []
    for path in sorted(source_dir.glob("*.pdf")):
        reader = PdfReader(str(path))
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").replace("\x00", " ").strip()
            if text:
                documents.append({
                    "source": path.name,
                    "page": page_number,
                    "text": text,
                })
    return documents
