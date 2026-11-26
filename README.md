Policy Assistant RAG

A policy assistant that answers from bank policies and cites the exact section, or says it doesn't know.

Project Overview

This is a learning project that demonstrates Retrieval-Augmented Generation (RAG) using fictional Example Bank policies.

The assistant retrieves relevant policy sections, provides them to a local language model, and generates answers with source citations.

RAG Pipeline

INGESTION
policies.py
    ↓
Chunk by section + metadata
    ↓
Embeddings
    ↓
Chroma Vector Database (rag_db)

ANSWERING
User Question
    ↓
Hybrid Search (BM25 + Semantic Search)
    ↓
Top-K Retrieved Chunks
    ↓
Numbered Sources [S1], [S2]...
    ↓
LLM generates JSON answer
    ↓
Python validates citations
    ↓
Answer + Sources OR Safe Fallback

Project Structure

policy-assistant-rag/
│
├── policies.py
├── rag_ingest.py
├── rag_retrieve.py
├── rag_answer.py
├── rag_eval.py
├── llm_config.py
├── embed_basics.py
├── requirements.txt
├── .gitignore
└── README.md

Technologies Used

Python

Ollama (local LLM)

ChromaDB

Pydantic

Requests

Nomic Embeddings

BM25 and Semantic Search

Installation

1. Clone the repository

git clone https://github.com/Anjali2887/policy-assistant-rag

cd policy-assistant-rag

2. Create and activate a virtual environment

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Start Ollama

Make sure Ollama is running and the configured model and embedding model are available.

5. Build the policy database

python rag_ingest.py

6. Ask questions

python rag_answer.py

Windows users

This project was tested using Ubuntu on WSL. If ChromaDB causes issues on Windows, run the Python files inside WSL Ubuntu. Ollama can continue running on Windows and can be accessed from WSL at localhost:11434, as configured in the course environment.

Design Decisions

Chunk by section: Each policy section becomes a separate chunk, preserving its heading and metadata.

Hybrid search: Combines BM25 keyword search and semantic vector search.

Reciprocal Rank Fusion (RRF): Combines rankings from keyword and semantic search.

Citation checks: Python verifies that cited source labels were actually retrieved.

Rebuild on change: Rebuilds the Chroma database after policy updates to avoid stale or duplicate policy versions.

Grounded answers: The model is instructed to answer only from retrieved sources and use a safe fallback when the sources do not answer the question.

Lab 3 — Evaluation Results

Record your actual hit@3 results from rag_eval.py.

Search Method

Hit@3 Before

Hit@3 After

Keyword

Add result

Add result

Semantic

Add result

Add result

Hybrid

Add result

Add result

Replace the placeholders with your actual Lab 3 measurements.

Known Limits and Next Steps

No reranker has been implemented yet.

Citation validation checks whether a source label was retrieved; it does not automatically verify whether the source supports the answer.

A small local language model is used, so answer quality may vary.

The system can still produce an unsupported answer when a retrieved source is related but does not actually support the question. For example, an unauthorised UPI transaction question received an answer from the policy about money sent to the wrong person. The citation label was valid, but the answer was not supported by that source.

Future improvements: add a reranker, permission filters, an LLM judge for citation support, and monitoring.

Disclaimer

This is a learning project built using fictional banking policy data. It is not a production banking system and must not be used for real banking decisions.