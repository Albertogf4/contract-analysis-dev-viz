from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..config import ChunkConfig

def load_pdf_text(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    return "".join(p.page_content for p in pages)

def chunk_text(text: str, cfg: ChunkConfig) -> List[str]:
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name=cfg.model_name,
        chunk_size=cfg.chunk_size,
        chunk_overlap=cfg.chunk_overlap,
    )
    return splitter.split_text(text)

def build_chunks_from_pdf(pdf_path: str, cfg: ChunkConfig) -> List[str]:
    return chunk_text(load_pdf_text(pdf_path), cfg)
