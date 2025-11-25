# app/preprocessing.py
import uuid
import os
from typing import Optional

from .models import ParsedPage, ParsedDocument


def parse_pdf_to_document(file_path: str, document_id: Optional[str] = None) -> ParsedDocument:
    """
    Placeholder that will call Llamaparse later.

    For now:
    - Reads the file bytes
    - Decodes them best-effort as a single big page of text

    Later:
    - Replace this with a proper Llamaparse client that returns text per page.
    """
    if document_id is None:
        document_id = str(uuid.uuid4())

    # TODO: replace with Llamaparse call
    with open(file_path, "rb") as f:
        raw_bytes = f.read()

    text = raw_bytes.decode(errors="ignore")

    page = ParsedPage(page_number=1, text=text)
    return ParsedDocument(
        document_id=document_id,
        filename=os.path.basename(file_path),
        pages=[page],
    )
