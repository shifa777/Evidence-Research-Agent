# 🔎 Evidence-Based AI Research Agent

An AI research agent that answers questions only from a provided collection of research documents, using semantic retrieval, evidence-grounded LLM synthesis, and source/page citations.

Built as a submission for the Rooman Technologies — Junior AI Research Associate 24-Hour AI Agent Challenge.

---

## 🎯 What This Agent Does

The agent takes:

* a research question
* a collection of source PDFs

and produces:

* a concise synthesized answer
* citations to the source document and page
* the retrieved evidence used to generate the answer
* an explicit **"Insufficient Evidence"** response when the provided sources do not contain enough relevant information

### In one sentence

> My agent takes a research question and a set of source documents and produces an evidence-grounded answer with source and page citations.

---

## 🧠 How It Works

The agent follows an evidence-first pipeline:

```text
                  User Question
                        │
                        ▼
              ┌──────────────────┐
              │ Research Question│
              └────────┬─────────┘
                       │
                       ▼
              Semantic Embedding
                       │
                       ▼
             ┌────────────────────┐
             │  Evidence Corpus   │
             │                    │
             │ UNESCO             │
             │ UNESCO             │
             │ U.S. DoE           │
             │ NIST               │
             └─────────┬──────────┘
                       │
                       ▼
              Relevant Chunks
                       │
                       ▼
              Similarity Ranking
                       │
              ┌────────┴─────────┐
              │                  │
        Enough evidence     Not enough evidence
              │                  │
              ▼                  ▼
        Gemma 3 synthesis   Insufficient Evidence
              │
              ▼
       Grounded Answer
              │
              ▼
       Source + Page Citations
```

The important design decision is that the LLM is not treated as the source of truth.

The retrieval system first determines what evidence is relevant. The LLM then synthesizes an answer from that evidence.

---

## 📚 Source Corpus

The repository contains real research publications rather than placeholder or dummy documents.

Current source corpus:

```text
data/
└── sources/
    ├── 01_UNESCO_Generative_AI_Guidance_2023.pdf
    ├── 02_UNESCO_AI_Competency_Framework_Students_2024.pdf
    ├── 03_US_DoE_AI_Future_Teaching_Learning_2023.pdf
    └── 04_NIST_AI_RMF_1.0.pdf
```

The corpus covers topics including:

* Generative AI
* AI in education
* AI competencies
* Teaching and learning
* Responsible AI
* AI risks
* Trustworthy AI
* AI risk management

The sources are included in the repository so that a reviewer can reproduce the demo without needing to find or download the documents separately.

See `SOURCE_LICENSES.md` for attribution and source-document information.

---

## 🛠️ Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Language             | Python 3.10+          |
| UI                   | Streamlit             |
| PDF extraction       | pypdf                 |
| Embeddings           | Sentence Transformers |
| Embedding model      | all-MiniLM-L6-v2      |
| Similarity           | Cosine similarity     |
| LLM runtime          | Ollama                |
| LLM                  | Gemma 3 4B            |
| Numerical operations | NumPy                 |
| Testing              | pytest                |
| Version control      | Git / GitHub          |

---

## 📁 Project Structure

```text
rooman_research_agent/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── SOURCE_LICENSES.md
│
├── data/
│   ├── questions.json
│   │
│   └── sources/
│       ├── 01_UNESCO_Generative_AI_Guidance_2023.pdf
│       ├── 02_UNESCO_AI_Competency_Framework_Students_2024.pdf
│       ├── 03_US_DoE_AI_Future_Teaching_Learning_2023.pdf
│       └── 04_NIST_AI_RMF_1.0.pdf
│
├── outputs/
│   └── sample_answers.md
│
├── src/
│   ├── citation.py
│   ├── chunker.py
│   ├── config.py
│   ├── document_loader.py
│   ├── main.py
│   ├── ollama_client.py
│   ├── pipeline.py
│   ├── researcher.py
│   └── retriever.py
│
└── tests/
    └── test_agent.py
```

### Important Files

**`app.py`**
The Streamlit interface used by the reviewer.

**`document_loader.py`**
Reads PDF documents page-by-page while preserving source and page metadata.

**`chunker.py`**
Splits extracted document text into retrieval-friendly evidence chunks.

**`retriever.py`**
Creates semantic embeddings and ranks evidence using cosine similarity.

**`researcher.py`**
Coordinates retrieval, evidence validation, LLM synthesis, and result generation.

**`ollama_client.py`**
Connects the application to the locally running Gemma model.

**`citation.py`**
Handles source/page citation formatting.

**`questions.json`**
Contains the reproducible question set for the challenge.

---

# ⚡ Quick Start

## 1. Clone the Repository

```bash
git clone https://github.com/shifa777/Evidence-Research-Agent
cd rooman_research_agent
```

Or download the repository as a ZIP and open the extracted folder in VS Code.

---

## 2. Check Python

Recommended:

```bash
python --version
```

Python 3.10–3.13 is supported by the project dependencies.

If your machine has multiple Python installations, use:

```bash
py --version
```

and, when needed:

```bash
py -3.13 -m venv venv
```

Using a virtual environment is strongly recommended.

---

## 3. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run this only for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

You should see:

```text
(venv)
```

at the beginning of the terminal prompt.

### Verify the Environment

Run:

```bash
python -c "import sys; print(sys.executable)"
```

The output should point to:

```text
...\rooman_research_agent\venv\Scripts\python.exe
```

This check prevents packages from accidentally being installed into the system Python installation.

---

## 4. Install Project Dependencies

Upgrade pip inside the virtual environment:

```bash
python -m pip install --upgrade pip
```

Then install the complete dependency set:

```bash
python -m pip install -r requirements.txt
```

Using:

```bash
python -m pip
```

instead of simply:

```bash
pip
```

helps ensure packages are installed into the same Python environment that will run the application.

### Verify the Critical Dependencies

```bash
python -c "import streamlit, pypdf, sentence_transformers, numpy; print('All core dependencies are installed.')"
```

Expected:

```text
All core dependencies are installed.
```

---

## 5. Install Ollama

This project uses Ollama to run the LLM locally.

Install Ollama from:

https://ollama.com/

After installation, verify:

```bash
ollama --version
```

---

## 6. Download the LLM

Pull the model used by this project:

```bash
ollama pull gemma3:4b
```

Verify:

```bash
ollama list
```

You should see:

```text
gemma3:4b
```

Ollama must be running when the research question is submitted.

---

## 7. Configure Environment Variables

Copy the example configuration:

```powershell
Copy-Item .env.example .env
```

This project uses a local Ollama server, so no OpenAI, Groq, or Anthropic API key is required.

The default Ollama configuration is:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:4b
```

Do not commit `.env` to GitHub.

The repository's `.gitignore` excludes it.

---

## 8. Run the Application

Recommended Windows command:

```bash
python -m streamlit run app.py
```

You should see:

```text
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

Open:

http://localhost:8501

---

# 🧪 Sample Input Questions

Use questions related to the included source corpus.

### Test 1 — Generative AI

> What are the major risks and challenges of generative AI in education?

### Test 2 — Student Competencies

> What AI competencies should students develop?

### Test 3 — Teaching and Learning

> How can AI affect teaching and learning?

### Test 4 — Trustworthy AI

> What trustworthy AI characteristics are emphasized by NIST?

### Test 5 — Responsible AI

> What principles should guide responsible use of AI in education?

---

# 📊 Sample Output

The following is an example of the output generated by the research agent.

### Answer

> Generative AI can create challenges related to accuracy, bias, privacy, academic integrity, and the need for appropriate human oversight in educational settings.

### Evidence

* UNESCO — Generative AI Guidance, p. 14
* UNESCO — Generative AI Guidance, p. 18

### Citations

```text
[1] UNESCO, Guidance for Generative AI in Education and Research, p. 14
[2] UNESCO, Guidance for Generative AI in Education and Research, p. 18
```

The sample demonstrates that the agent provides a grounded answer, supporting evidence, and page-level citations.

---

# 🚫 Insufficient Evidence Example

The agent is designed to avoid generating answers when the provided source corpus does not contain enough relevant evidence.

### Question

> What is the use of docker?

### Expected Output

```text
INSUFFICIENT EVIDENCE

The provided sources do not contain enough evidence to answer this question.
```

The agent does not use the LLM's general knowledge when the provided sources do not contain sufficient evidence.

---

# 📦 Agent-Specific Deliverables

This project implements the required deliverables for the Research Agent with Citations.

### 1. Research Question

The agent accepts a natural-language research question from the user.

### 2. Source Documents

The agent works with a provided collection of research PDFs stored in:

```text
data/sources/
```

### 3. Relevant Evidence Retrieval

The system uses semantic embeddings and cosine similarity to retrieve the most relevant passages from the source documents.

### 4. Evidence-Grounded Answer

The retrieved evidence is passed to the local Gemma 3 model through Ollama to generate a concise research answer.

### 5. Source and Page Citations

The system preserves document and page metadata throughout the retrieval pipeline and provides source/page citations with the generated answer.

### 6. Insufficient Evidence Detection

The system checks whether the retrieved evidence is relevant enough to answer the question. If sufficient evidence is not available, it returns an explicit **Insufficient Evidence** response instead of relying on unsupported model knowledge.

### 7. Reproducible Question Set

A predefined set of research questions is provided in:

```text
data/questions.json
```

### 8. Sample Answers

Example outputs are provided in:

```text
outputs/sample_answers.md
```

### 9. Runnable Interface

The complete research agent can be launched through:

```text
app.py
```

using Streamlit.

### 10. Automated Tests

Core agent functionality is covered by tests in:

```text
tests/test_agent.py
```

---

# 🔬 Retrieval Approach

The retrieval pipeline works in several stages.

## 1. Document Loading

Each PDF is read page-by-page.

The system preserves:

* source document
* page number
* page text

This metadata allows citations to point back to the original document.

---

## 2. Chunking

Long PDF pages are divided into smaller evidence chunks.

Each chunk keeps its original source and page metadata.

Conceptually:

```text
PDF
 ↓
Page
 ↓
Evidence chunks
 ↓
Embedding
```

---

## 3. Semantic Embeddings

Each evidence chunk is converted into a vector using:

```text
all-MiniLM-L6-v2
```

The user's research question is converted into an embedding using the same model.

---

## 4. Similarity Ranking

The system compares the question embedding with the evidence embeddings using cosine similarity.

The highest-relevance chunks become the evidence supplied to the answer-generation stage.

This means the LLM does not need to receive every page of every PDF.

---

# 🤖 LLM Generation

The retrieved evidence is passed to:

```text
Gemma 3 4B
```

through Ollama.

The model is instructed to:

* Use the supplied evidence.
* Answer the user's question.
* Avoid unsupported claims.
* Use the supplied source identifiers.
* State when the evidence is insufficient.

The LLM is therefore primarily used for synthesis and explanation, while retrieval determines the evidence.

---

# 📌 Citation Design

Each retrieved chunk contains metadata such as:

```text
source = UNESCO PDF
page = 14
```

The application preserves this metadata throughout the pipeline.

Citations therefore identify:

* source document
* page number

rather than relying on the LLM to invent page numbers.

The UI also exposes the retrieved passages so a reviewer can inspect the evidence behind the answer.

---

# 🧪 Testing

Run:

```bash
pytest -q
```

The tests verify core retrieval and processing behavior.

The goal is to catch implementation errors without requiring the UI for every test.

---

# ⚖️ Design Tradeoffs

## Why Local Ollama?

A local LLM avoids requiring the reviewer to obtain an external API key.

### Advantages

* No paid API requirement
* No API key in the repository
* Source documents remain local
* Reproducible demonstration environment

### Tradeoffs

* Requires the reviewer to install Ollama
* Local inference is slower than many hosted APIs
* Model quality depends on available hardware

---

## Why Sentence Transformers?

Semantic embeddings allow the system to retrieve passages based on meaning rather than requiring exact keyword matches.

For example, a question and a passage can be relevant even when they use slightly different wording.

### Tradeoffs

* Embedding models add a first-run download
* Semantic similarity is not perfect
* Retrieval thresholds require tuning

---

## Why Not Send the Entire PDF to the LLM?

Sending every document in full would:

* Increase context size
* Increase latency
* Make evidence selection less explicit
* Make the system less efficient

Retrieval narrows the context to passages relevant to the question.

---

## Why Show Retrieved Evidence?

A final answer alone does not demonstrate that the system actually performed research.

Displaying the retrieved evidence allows the reviewer to inspect:

```text
Question
   ↓
Retrieved passage
   ↓
Generated answer
   ↓
Citation
```

This improves transparency and makes the system easier to evaluate.

---

# 🚀 Future Improvements

With more development time, the system could be extended with:

* PDF/DOCX/TXT upload through the UI
* OCR for scanned documents
* Persistent vector database
* Hybrid keyword + semantic retrieval
* Reranking models
* Sentence-level citations
* Web search as an optional research tool
* Citation validation
* Document-level source filtering
* Conversation history
* Evaluation benchmarks for retrieval accuracy
* Automated hallucination/grounding evaluation

These are intentionally outside the minimum challenge scope so that the core end-to-end agent remains simple and reproducible.

---

# 🔐 Security & Configuration

Do not commit:

```text
.env
venv/
__pycache__/
```

No external API key is required for the default configuration.

The LLM runs through the local Ollama service.

Never commit private API keys, access tokens, passwords, or other secrets to GitHub.

---

# 🛠️ Troubleshooting

## ModuleNotFoundError: No module named 'pypdf'

Run:

```bash
python -m pip install -r requirements.txt
```

Then verify:

```bash
python -c "import pypdf; print(pypdf.__version__)"
```

If it still fails, verify that your virtual environment is active:

```bash
python -c "import sys; print(sys.executable)"
```

The path should contain:

```text
venv\Scripts\python.exe
```

---

## ModuleNotFoundError: No module named 'sentence_transformers'

Run:

```bash
python -m pip install -r requirements.txt
```

Then:

```bash
python -c "import sentence_transformers; print('sentence-transformers OK')"
```

---

## Streamlit Starts but the Application Crashes

First verify all core dependencies:

```bash
python -c "import streamlit, pypdf, sentence_transformers, numpy; print('Dependencies OK')"
```

Then start Streamlit with:

```bash
python -m streamlit run app.py
```

Using `python -m streamlit` makes it explicit which Python environment is running Streamlit.

---

## ollama Command Not Found

Install Ollama and restart the terminal.

Then:

```bash
ollama --version
```

---

## Ollama Connection Error

Make sure Ollama is running.

Then test:

```bash
ollama list
```

Verify that:

```text
gemma3:4b
```

is installed.

---

## gemma3:4b Is Missing

Run:

```bash
ollama pull gemma3:4b
```

---

## First Run Appears Slow

This is expected if:

* the embedding model is downloading
* PDFs are being indexed
* Ollama is loading Gemma for the first time

Allow the first run to complete.

---

## Hugging Face Warning

You may see:

```text
Warning: You are sending unauthenticated requests to the HF Hub...
```

This is a warning about Hugging Face request limits.

It does not mean the application has failed.

The project does not require a Hugging Face token for the normal demo.

---

## PowerShell Activation Error

If you see a script execution policy error:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

The Process scope means the change applies only to the current PowerShell session.

---

# 👩‍💻 Reviewer Quick Start

If everything is already installed:

```bash
git clone https://github.com/shifa777/Evidence-Research-Agent
cd rooman_research_agent

python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

ollama pull gemma3:4b

python -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

### Recommended first question:

> What are the major risks and challenges of generative AI in education?

### Recommended evidence-boundary test:

> What is the use of docker?

---

# 📊 Project Goal

The goal of this project is not to build the largest possible research system.

The goal is to demonstrate a complete and explainable agent:

```text
Question
   ↓
Retrieve
   ↓
Reason over evidence
   ↓
Generate
   ↓
Cite
   ↓
Detect insufficient evidence
```

The implementation prioritizes working functionality, reproducibility, transparent retrieval, and honest limitations over unnecessary complexity.
