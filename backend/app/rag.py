from typing import List, Optional

from .config import Settings
from .models import RAGResult
from .preprocessing import parse_pdf_to_document_pypdf2
from .chunking import chunk_parsed_document
from .vectorstore import ChromaVectorStore
from .embeddings import OpenAILLMClient
from .graph_builder import KnowledgeGraphBuilder
from .knowledge_graph import KnowledgeGraphStore
from .graph_context import GraphContextRetriever


class DocumentIndexer:
    def __init__(self, settings: Settings, 
                 vector_store: ChromaVectorStore, 
                 graph_builder: Optional[KnowledgeGraphBuilder] = None,
                 graph_store: Optional[KnowledgeGraphStore] = None,
                ):
        self.settings = settings
        self.vector_store = vector_store
        self.graph_builder = graph_builder
        self.graph_store = graph_store

    def index_pdf(self, file_path: str, document_id: Optional[str] = None) -> str:
        # 1. Parse PDF (stub -> Llamaparse in future)
        parsed_doc = parse_pdf_to_document_pypdf2(file_path, document_id=document_id)

        # 2. Chunk
        chunks = chunk_parsed_document(parsed_doc, self.settings)

        # 3. Store in vector DB
        self.vector_store.add_chunks(chunks)

        # 4. Build and store knowledge graph (optional)
        if self.graph_builder is not None and self.graph_store is not None:
            graph = self.graph_builder.build_graph(parsed_doc)
            self.graph_store.save_graph(graph)

        return parsed_doc.document_id


class RAGPipeline:
    def __init__(
        self,
        settings: Settings,
        vector_store: ChromaVectorStore,
        llm_client: OpenAILLMClient,
        graph_context_retriever: Optional[GraphContextRetriever] = None
    ):
        self.settings = settings
        self.vector_store = vector_store
        self.llm_client = llm_client
        self.graph_context_retriever = graph_context_retriever

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

        # 3. Build graph context
        graph_context: Optional[str] = None
        if self.graph_context_retriever is not None:
            graph_context = self.graph_context_retriever.build_graph_context(
                question=question,
                document_id=document_id,
                
            )

        # 4. Ask LLM
        answer = self.llm_client.generate_answer(question, context_blocks, graph_context=graph_context)

        return RAGResult(answer=answer, context_chunks=retrieved_chunks)
