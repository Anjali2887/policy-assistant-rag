"""Chapter 2: turn text into vectors and compare meanings.  Run: python embed_basics.py"""
import math

import requests

from llm_config import EMBED_MODEL, OPTIONS

EMBED_URL = "http://localhost:11434/api/embed"


def embed(texts: list[str]) -> list[list[float]]:
    """Send a list of texts, get back one vector (list of floats) per text."""
    resp = requests.post(
        EMBED_URL,
        json={"model": EMBED_MODEL, "input": texts, "options": OPTIONS},
        timeout=300,
    )
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data["embeddings"]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """1.0 = same direction (same meaning), 0 = unrelated."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    sentences = [
        "My card was charged twice for one purchase.",
        "I see a duplicate debit on my credit card.",
        "What is the interest rate on a fixed deposit?",
    ]
    vectors = embed(sentences)
    print(f"Each sentence became {len(vectors[0])} numbers. First five: {vectors[0][:5]}")

    print("Similarity 1 vs 2 (same meaning):", round(cosine_similarity(vectors[0], vectors[1]), 3))
    print("Similarity 1 vs 3 (different):   ", round(cosine_similarity(vectors[0], vectors[2]), 3))
