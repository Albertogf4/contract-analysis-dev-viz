# app/models.py
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ParsedPage:
    page_number: int
    text: str


@dataclass
class ParsedDocument:
    document_id: str
    filename: str
    pages: List[ParsedPage]


@dataclass
class Chunk:
    id: str
    document_id: str
    filename: str
    page_number: int
    text: str
    start_char: int
    end_char: int


@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    filename: str
    page_number: int
    start_char: int
    end_char: int
    text: str
    score: float  # similarity or distance


@dataclass
class RAGResult:
    answer: str
    context_chunks: List[RetrievedChunk]
