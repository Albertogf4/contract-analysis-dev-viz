from dataclasses import dataclass
import os


@dataclass
class Settings:
    # OpenAI
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    embedding_model: str = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
    llm_model: str = os.environ.get("LLM_MODEL", "gpt-4.1-mini")

    # Storage
    chroma_db_dir: str = os.environ.get("CHROMA_DB_DIR", "./chroma_db")
    upload_dir: str = os.environ.get("UPLOAD_DIR", "./uploads")
    collection_name: str = os.environ.get("CHROMA_COLLECTION_NAME", "documents")

    # RAG defaults
    top_k: int = int(os.environ.get("RAG_TOP_K", "4"))
    chunk_size: int = int(os.environ.get("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.environ.get("CHUNK_OVERLAP", "200"))

    # Knowledge graph
    graph_dir: str = os.environ.get("GRAPH_DIR", "./graphs")
    graph_max_chars: int = int(os.environ.get("GRAPH_MAX_CHARS", "12000"))
    # how many nodes from the graph to include in the prompt
    graph_context_top_k_nodes: int = int(os.environ.get("GRAPH_CONTEXT_TOP_K_NODES", "5"))