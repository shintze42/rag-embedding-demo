# rag-embedding-demo
Learning RAG: Building a semantic search system with embeddings and vector databases"

# RAG Embedding Demo

Learning to build Retrieval-Augmented Generation (RAG) systems using embeddings and vector databases.

## What This Does

This project demonstrates semantic search using:
- **LM Studio** - Local embedding model (nomic-embed-text)
- **Qdrant** - Vector database for storing embeddings
- **Python** - Orchestrating the embedding and search pipeline

### Key Features
- Converts text into 768-dimensional embeddings
- Stores embeddings in Qdrant with metadata
- Searches for semantically similar text (not just keyword matching)
- Returns results ranked by cosine similarity

## Files

- `main.py` - Stores multiple sentences as embeddings in Qdrant
- `search.py` - Searches for similar embeddings based on a query

## How It Works

1. **Storage (`main.py`)**: Takes sentences, converts them to embeddings via LM Studio, stores in Qdrant
2. **Search (`search.py`)**: Takes a search query, converts to embedding, finds most similar stored embeddings

## Setup

### Prerequisites
- Docker (for Qdrant)
- LM Studio with nomic-embed-text model
- Python 3.12+
- uv package manager

### Running

1. Start Qdrant:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

2. Start LM Studio with nomic-embed-text model

3. Store embeddings:
```bash
uv run main.py
```

4. Search:
```bash
uv run search.py
```

## Learning Goals

Part of a 12-week plan to learn AI/RAG systems for a career transition into AI strategy/product roles.

**Current Status**: Week 2 complete - Understanding embeddings and vector databases ✅
