# app/rag.py
from typing import List

from .config import Settings
from .models import RAGResult
from .preprocessing import parse_pdf_to_document
from .chunking import chunk_parsed_document
from .vectorstore import ChromaVectorStore
from .embeddings import OpenAILLMClient


class DocumentIndexer:
    def __init__(self, settings: Settings, vector_store: ChromaVectorStore):
        self.settings = settings
        self.vector_store = vector_store

    def index_pdf(self, file_path: str) -> str:
        # 1. Parse PDF (stub -> Llamaparse in future)
        parsed_doc = parse_pdf_to_document(file_path)

        # 2. Chunk
        chunks = chunk_parsed_document(parsed_doc, self.settings)

        # 3. Store in vector DB
        self.vector_store.add_chunks(chunks)

        return parsed_doc.document_id


class RAGPipeline:
    def __init__(
        self,
        settings: Settings,
        vector_store: ChromaVectorStore,
        llm_client: OpenAILLMClient,
    ):
        self.settings = settings
        self.vector_store = vector_store
        self.llm_client = llm_client

    def answer_question(self, question: str, document_id: str) -> RAGResult:
        # 1. Retrieve relevant chunks for that document
        retrieved_chunks = self.vector_store.query(
            query_text=question,
            top_k=self.settings.top_k,
            document_id=document_id,
        )

        # 2. Build context for LLM
        context_blocks: List[str] = []
        for rc in retrieved_chunks:
            header = (
                f"[doc_id={rc.document_id}, file={rc.filename}, "
                f"page={rc.page_number}, chars={rc.start_char}-{rc.end_char}]"
            )
            context_blocks.append(f"{header}\n{rc.text}")

        # 3. Ask LLM
        answer = self.llm_client.generate_answer(question, context_blocks)

        return RAGResult(answer=answer, context_chunks=retrieved_chunks)
