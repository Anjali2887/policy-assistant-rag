"""Chapter 3, step 3: answer from the retrieved chunks, with citations your code checks.
Run:  python rag_answer.py   (type a question; an empty line quits)
"""
import re

import requests
from pydantic import BaseModel, ValidationError

from llm_config import MODEL, OPTIONS
from rag_retrieve import CHUNK_BY_ID, hybrid_search

CHAT_URL = "http://localhost:11434/api/chat"
FALLBACK = "I can't find this in our policies. I'll check with our team."

SYSTEM = (
    "You are a support assistant for Example Bank. Answer ONLY from the numbered sources. "
    "After each fact, cite its source like [S1]. If the sources do not answer the question, "
    f'reply exactly "{FALLBACK}" with an empty citations list.If the sources are about a different product or customer type than the question, use the fallback.Reply only with JSON.'
)


class RagAnswer(BaseModel):
    answer: str
    citations: list[str]  # source labels, e.g. ["S1", "S3"]


def build_context(chunk_ids: list[str]) -> tuple[str, dict[str, str]]:
    """Number the chunks [S1], [S2] ... and remember which label is which chunk."""
    labels = {f"S{i}": chunk_id for i, chunk_id in enumerate(chunk_ids, start=1)}
    lines = [f"[{label}] {CHUNK_BY_ID[chunk_id]['text']}" for label, chunk_id in labels.items()]
    return "\n".join(lines), labels


def ask(question: str, k: int = 8) -> dict:
    context, labels = build_context(hybrid_search(question, k=k))
    resp = requests.post(
        CHAT_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": f'Sources:\n"""\n{context}\n"""\n\nQuestion: {question}'},
            ],
            "stream": False,
            "format": RagAnswer.model_json_schema(),
            "options": {**OPTIONS, "temperature": 0, "seed": 42, "num_ctx": 4096, "num_predict": 300},
        },
        timeout=600,
    )
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    try:
        result = RagAnswer.model_validate_json(data["message"]["content"])
    except ValidationError:
        return {"answer": FALLBACK, "sources": [], "problem": "the model did not return valid JSON"}

    if result.answer.strip() == FALLBACK:
        return {"answer": FALLBACK, "sources": [], "problem": None}
    cited = sorted(set(result.citations) | set(re.findall(r"\[(S\d+)\]", result.answer)))
    if not cited:
        return {"answer": FALLBACK, "sources": [], "problem": "the answer had no citations"}
    unknown = [c for c in cited if c not in labels]
    if unknown:
        return {"answer": FALLBACK, "sources": [], "problem": f"it cited sources it was never given: {unknown}"}

    sources = []
    for label in cited:
        meta = CHUNK_BY_ID[labels[label]]["metadata"]
        sources.append(f"[{label}] {meta['title']} > {meta['section']} (version {meta['version']})")
    return {"answer": result.answer, "sources": sources, "problem": None}


if __name__ == "__main__":
    print("Example Bank policy assistant. Ask a question (empty line to quit).")
    while True:
        question = input("\nQuestion: ").strip()
        if not question:
            break
        reply = ask(question)
        print("\nAnswer:", reply["answer"])
        for source in reply["sources"]:
            print("  source:", source)
        if reply["problem"]:
            print("  [guardrail]", reply["problem"])
