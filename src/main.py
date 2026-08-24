import argparse
import json
from .ollama_client import OllamaClient
from .pipeline import build_retriever
from .researcher import answer_question


def main():
    parser = argparse.ArgumentParser(description="Evidence-Based AI Research Agent")
    parser.add_argument("--question", type=str, help="Research question")
    args = parser.parse_args()

    print("Loading source documents and building the retrieval index...")
    retriever, pages, chunks = build_retriever()
    print(f"Indexed {pages} PDF pages into {chunks} evidence chunks.")

    llm = OllamaClient()
    try:
        models = llm.health()
        if llm.model not in models and not any(m.startswith(llm.model.split(":")[0] + ":") for m in models):
            raise RuntimeError(f"Ollama model '{llm.model}' is not installed. Run: ollama pull {llm.model}")
    except Exception as exc:
        raise SystemExit(f"Ollama is not ready: {exc}")

    question = args.question or input("\nResearch question: ").strip()
    if not question:
        raise SystemExit("A research question is required.")

    result = answer_question(question, retriever, llm)
    print("\n" + "=" * 72)
    print("EVIDENCE-BASED RESEARCH AGENT")
    print("=" * 72)
    print(f"\nQuestion: {question}\n")
    print(result["answer"])
    if result["citations"]:
        print("\nSources:")
        for citation in result["citations"]:
            print(f"- {citation}")
    print("\nRetrieval evidence:")
    for item in result["retrieved"][:6]:
        print(f"- {item['source']} | page {item['page']} | similarity {item['score']}")

    with open("outputs/latest_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
