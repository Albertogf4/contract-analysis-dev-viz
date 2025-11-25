# app/chunking.py
import uuid
from typing import List

from .models import ParsedDocument, Chunk
from .config import Settings


def chunk_parsed_document(
    doc: ParsedDocument,
    settings: Settings,
) -> List[Chunk]:
    chunks: List[Chunk] = []

    for page in doc.pages:
        text = page.text
        start = 0
        while start < len(text):
            end = min(start + settings.chunk_size, len(text))
            chunk_text = text[start:end]
            chunk_id = str(uuid.uuid4())

            chunks.append(
                Chunk(
                    id=chunk_id,
                    document_id=doc.document_id,
                    filename=doc.filename,
                    page_number=page.page_number,
                    text=chunk_text,
                    start_char=start,
                    end_char=end,
                )
            )

            if end == len(text):
                break
            start = end - settings.chunk_overlap

    return chunks
