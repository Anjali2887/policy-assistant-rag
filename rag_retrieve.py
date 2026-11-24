"""Chapter 3, step 2: find the best chunks with keyword, semantic and hybrid search.
Run it to compare the three:  python rag_retrieve.py
"""
import math
import re
from collections import Counter

from embed_basics import embed
from rag_ingest import get_collection, make_chunks

QUERY_PREFIX = "search_query: "  # nomic-embed-text expects this prefix on questions
CHUNKS = make_chunks()           # keyword search reads the same chunks that Chroma stores
CHUNK_BY_ID = {c["id"]: c for c in CHUNKS}


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def matches(metadata: dict, where: dict | None) -> bool:
    """Simple equality filter, e.g. {"category": "cards"}, so keyword search obeys it too."""
    return all(metadata.get(key) == value for key, value in (where or {}).items())


def keyword_search(query: str, k: int = 5, where: dict | None = None) -> list[str]:
    """BM25, the scoring behind Lucene and Elasticsearch. Rare shared words count most."""
    pool = [c for c in CHUNKS if matches(c["metadata"], where)]
    docs = [tokens(c["text"]) for c in pool]
    if not docs:
        return []
    avg_len = sum(len(d) for d in docs) / len(docs)
    doc_freq = Counter(word for d in docs for word in set(d))
    scored = []
    for chunk, words in zip(pool, docs):
        tf = Counter(words)
        score = 0.0
        for word in set(tokens(query)):
            if word in tf:
                idf = math.log(1 + (len(docs) - doc_freq[word] + 0.5) / (doc_freq[word] + 0.5))
                score += idf * tf[word] * 2.5 / (tf[word] + 1.5 * (0.25 + 0.75 * len(words) / avg_len))
        scored.append((score, chunk["id"]))
    scored.sort(reverse=True)
    return [chunk_id for score, chunk_id in scored[:k] if score > 0]


def semantic_search(query: str, k: int = 5, where: dict | None = None) -> list[str]:
    """Meaning-based search in Chroma."""
    collection = get_collection()
    res = collection.query(query_embeddings=embed([QUERY_PREFIX + query]), n_results=k, where=where)
    return res["ids"][0]


def hybrid_search(query: str, k: int = 4, where: dict | None = None) -> list[str]:
    """Reciprocal Rank Fusion (RRF): each list votes 1 / (60 + rank). Being near the top of both wins."""
    fused = Counter()
    for ranking in (semantic_search(query, 8, where), keyword_search(query, 8, where)):
        for rank, chunk_id in enumerate(ranking, start=1):
            fused[chunk_id] += 1 / (60 + rank)
    return [chunk_id for chunk_id, score in fused.most_common(k)]


if __name__ == "__main__":
    for query in ["someone used my card without my permission", "CRD-07", "Rs 50,000"]:
        print(f"\nQUERY: {query}")
        for name, search in [("keyword", keyword_search), ("semantic", semantic_search), ("hybrid", hybrid_search)]:
            print(f"  {name:8} -> {search(query, 3)}")
