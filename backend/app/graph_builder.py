from __future__ import annotations

from typing import List
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from .config import Settings
from .models import ParsedDocument
from .knowledge_graph import KnowledgeGraph, KGNode, KGEdge


class KnowledgeGraphBuilder:
    """
    Uses a ChatGPT model (via LangChain) to build a compact knowledge graph
    representing the core ideas of a document.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=0,
            api_key=settings.openai_api_key or None,
        )

    def _build_prompt(self, text: str) -> List:
        template = """
                You are an AI that extracts a simple knowledge graph from a document.

                Read the text and identify the core concepts, entities and how they relate.
                Return ONLY valid JSON with this structure (no explanation, no markdown):

                {{
                "nodes": [
                    {{
                    "id": "string (short, unique)",
                    "label": "human-readable name",
                    "type": "high-level type (e.g. 'entity', 'process', 'risk', 'metric')",
                    "description": "1-2 sentence summary in plain language"
                    }}
                ],
                "edges": [
                    {{
                    "id": "string (short, unique)",
                    "source": "node_id",
                    "target": "node_id",
                    "relation": "short verb phrase describing the relation"
                    }}
                ]
                }}

                Keep it compact (10-30 nodes, 10-50 edges). Focus on the main ideas of the document.

                TEXT:
                {text}
                """
        prompt = ChatPromptTemplate.from_template(template)
        return prompt.format_messages(text=text)

    def build_graph(self, doc: ParsedDocument) -> KnowledgeGraph:
        # Join pages and optionally truncate
        full_text = "\n\n".join(p.text for p in doc.pages)
        max_chars = self.settings.graph_max_chars
        if max_chars and len(full_text) > max_chars:
            full_text = full_text[:max_chars]

        messages = self._build_prompt(full_text)
        response = self.llm.invoke(messages)
        raw = response.content.strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Very defensive fallback: empty graph
            data = {"nodes": [], "edges": []}

        nodes = [KGNode(**n) for n in data.get("nodes", [])]
        edges = [KGEdge(**e) for e in data.get("edges", [])]

        return KnowledgeGraph(
            document_id=doc.document_id,
            nodes=nodes,
            edges=edges,
        )
