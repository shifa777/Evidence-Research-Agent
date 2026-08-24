import json
import streamlit as st
from pathlib import Path
from src.ollama_client import OllamaClient
from src.pipeline import build_retriever
from src.researcher import answer_question

st.set_page_config(page_title="Evidence-Based Research Agent", page_icon="🔎", layout="wide")

st.markdown("""
<style>
:root {
    --accent: #6C5CE7;
    --accent-soft: rgba(108, 92, 231, 0.12);
    --border: rgba(128,128,128,.18);
}

.block-container {max-width: 1100px; padding-top: 2rem; padding-bottom: 3rem;}

/* Hero */
.hero {
    padding: 2rem 2.2rem;
    border-radius: 20px;
    margin-bottom: 1.6rem;
    background: linear-gradient(135deg, var(--accent-soft), rgba(108,92,231,0.02));
    border: 1px solid var(--border);
}
.hero h1 {
    margin-bottom: .4rem;
    font-size: 2rem;
}
.hero p {
    margin: .2rem 0;
}
.small {opacity: .7; font-size: .92rem;}

/* Metric cards */
div[data-testid="stMetric"] {
    background: rgba(128,128,128,0.06);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: .9rem 1rem;
}
div[data-testid="stMetricValue"] {
    color: var(--accent);
}

/* Source cards / expanders */
.source-card {
    padding: 1rem;
    border: 1px solid var(--border);
    border-radius: 12px;
    margin: .5rem 0;
}
div[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: .5rem;
}

/* Buttons */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: .6rem 1rem;
    transition: transform 0.05s ease-in-out;
}
div.stButton > button:hover {
    border-color: var(--accent);
    color: var(--accent);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid var(--border);
}

/* Section headers */
h2, h3 {
    margin-top: 1.4rem;
}

hr {
    margin: 1.5rem 0;
    opacity: .4;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🔎 Evidence-Based AI Research Agent</h1>
<p>Ask a question. The agent retrieves evidence from the provided research documents, synthesizes an answer, and cites the source and page for the retrieved evidence.</p>
<p class="small">The model is instructed not to use outside knowledge and to refuse unsupported questions.</p>
</div>
""", unsafe_allow_html=True)

sources_dir = Path("data/sources")
sources = sorted(sources_dir.glob("*.pdf"))

with st.sidebar:
    st.header("📚 Research Corpus")
    st.write(f"**{len(sources)} source documents** included")
    for s in sources:
        st.caption(f"📄 {s.name}")
    st.divider()
    st.header("ℹ️ How to test")
    st.write("Use one of the example questions or ask your own question about the provided sources.")
    st.caption("Tip: Ask an unrelated question to test the insufficient-evidence behavior.")

@st.cache_resource(show_spinner="Building evidence index...")
def get_retriever():
    return build_retriever()

try:
    retriever, page_count, chunk_count = get_retriever()
except Exception as exc:
    st.error(f"Could not build the document index: {exc}")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Source documents", len(sources))
col2.metric("PDF pages", page_count)
col3.metric("Evidence chunks", chunk_count)

examples = [
    "What are the major risks and challenges of generative AI in education?",
    "What principles should guide responsible use of AI in education?",
    "What AI competencies should students develop?",
    "What does the U.S. Department of Education recommend about AI and teaching and learning?",
    "What trustworthy AI characteristics are emphasized by the NIST AI Risk Management Framework?",
    "What does the research say about quantum computing in banking?",
]

st.subheader("💡 Try an example")
selected = st.selectbox("Example questions", ["Choose a question..."] + examples)
question = st.text_area(
    "Research question",
    value="" if selected == "Choose a question..." else selected,
    height=100,
    placeholder="Example: What are the major risks and challenges of generative AI in education?",
)

run = st.button("🔍 Research", type="primary", use_container_width=True)

if run:
    if not question.strip():
        st.warning("Enter a research question first.")
        st.stop()
    llm = OllamaClient()
    try:
        llm.health()
    except Exception as exc:
        st.error(f"Ollama is not reachable. Start Ollama and install the configured model. Details: {exc}")
        st.stop()
    with st.spinner("Retrieving evidence and synthesizing the answer..."):
        result = answer_question(question.strip(), retriever, llm)
    st.divider()
    if result["status"] == "insufficient_evidence":
        st.warning("Insufficient evidence")
        st.write(result["answer"])
    else:
        st.subheader("✅ Answer")
        st.markdown(result["answer"])
        st.subheader("📎 Retrieved evidence")
        for i, item in enumerate(result["retrieved"], start=1):
            with st.expander(f"S{i} · {item['source']} · page {item['page']} · similarity {item['score']:.3f}"):
                st.write(item["text"])
        st.subheader("🔗 Sources")
        for c in result["citations"]:
            st.write(f"- {c}")
        st.download_button(
            "⬇️ Download result JSON",
            data=json.dumps(result, indent=2, ensure_ascii=False),
            file_name="research_result.json",
            mime="application/json",
        )