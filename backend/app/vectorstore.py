# app/vectorstore.py
from typing import List, Optional, Dict, Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from .config import Settings
from .models import Chunk, RetrievedChunk
from .embeddings import OpenAIEmbeddingClient


class ChromaVectorStore:
    def __init__(self, settings: Settings, embedder: OpenAIEmbeddingClient):
        self.settings = settings
        self.embedder = embedder

        self.client = chromadb.PersistentClient(
            path=settings.chroma_db_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: List[Chunk]) -> None:
        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed(texts)

        ids = [c.id for c in chunks]
        metadatas: List[Dict[str, Any]] = [
            {
                "chunk_id": c.id,
                "document_id": c.document_id,
                "filename": c.filename,
                "page_number": c.page_number,
                "start_char": c.start_char,
                "end_char": c.end_char,
            }
            for c in chunks
        ]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

    def query(
        self,
        query_text: str,
        top_k: int,
        document_id: Optional[str] = None,
    ) -> List[RetrievedChunk]:
        query_embedding = self.embedder.embed([query_text])[0]

        where_filter = {"document_id": document_id} if document_id else None

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
        )

        retrieved: List[RetrievedChunk] = []

        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]  # lower is more similar for cosine

        for doc_id, text, meta, distance in zip(ids, docs, metas, distances):
            retrieved.append(
                RetrievedChunk(
                    chunk_id=meta.get("chunk_id", doc_id),
                    document_id=meta["document_id"],
                    filename=meta["filename"],
                    page_number=meta["page_number"],
                    start_char=meta["start_char"],
                    end_char=meta["end_char"],
                    text=text,
                    score=float(distance),
                )
            )

        return retrieved
