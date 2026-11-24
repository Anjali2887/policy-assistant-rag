"""Chapter 3, step 1: chunk the policies by section, embed the chunks, store them in Chroma.
Run it once, and again whenever you change policies.py:  python rag_ingest.py
"""
import shutil
from pathlib import Path

import chromadb

from embed_basics import embed
from policies import POLICIES

DB_PATH = "./rag_db"
DOC_PREFIX = "search_document: "  # nomic-embed-text expects this prefix on stored text


def make_chunks() -> list[dict]:
    """One chunk per policy section. The title and heading stay inside the chunk text."""
    chunks = []
    for doc in POLICIES:
        for n, (heading, body) in enumerate(doc["sections"], start=1):
            chunks.append({
                "id": f"{doc['id']}#{n}",
                "text": f"{doc['title']} > {heading}: {body}",
                "metadata": {"doc_id": doc["id"], "title": doc["title"], "section": heading,
                             "category": doc["category"], "version": doc["version"]},
            })
    return chunks


def get_collection(rebuild: bool = False):
    """Open the vector store. rebuild=True deletes it first, so re-running never duplicates."""
    if rebuild and Path(DB_PATH).exists():
        shutil.rmtree(DB_PATH)
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name="policy_chunks",
        embedding_function=None,  # we pass our own vectors from Ollama
        configuration={"hnsw": {"space": "cosine"}},
    )


if __name__ == "__main__":
    chunks = make_chunks()
    collection = get_collection(rebuild=True)
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embed([DOC_PREFIX + c["text"] for c in chunks]),
        metadatas=[c["metadata"] for c in chunks],
    )
    print(f"Stored {collection.count()} chunks from {len(POLICIES)} policies in {DB_PATH}")
