# app/graph_context.py
from __future__ import annotations

from math import sqrt
from typing import List, Optional

from .config import Settings
from .knowledge_graph import KnowledgeGraphStore, KGNode
from .embeddings import OpenAIEmbeddingClient


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    den_a = sqrt(sum(x * x for x in a))
    den_b = sqrt(sum(y * y for y in b))
    if den_a == 0 or den_b == 0:
        return 0.0
    return num / (den_a * den_b)


class GraphContextRetriever:
    """
    Retrieves a compact, text-based context derived from the knowledge graph
    that is most relevant to a given question.
    """

    def __init__(
        self,
        settings: Settings,
        graph_store: KnowledgeGraphStore,
        embedder: OpenAIEmbeddingClient,
    ):
        self.settings = settings
        self.graph_store = graph_store
        self.embedder = embedder

    def build_graph_context(self, question: str, document_id: str) -> Optional[str]:
        graph = self.graph_store.load_graph(document_id)
        if graph is None or not graph.nodes:
            return None

        # 1) Prepare text representation for each node
        node_texts: List[str] = []
        for n in graph.nodes:
            desc = n.description or ""
            node_texts.append(
                f"Node {n.id} ({n.label}, type={n.type}): {desc}"
            )

        # 2) Embed question and nodes
        q_emb = self.embedder.embed([question])[0]
        node_embs = self.embedder.embed(node_texts)

        # 3) Rank nodes by similarity
        scored_nodes: List[tuple[KGNode, float]] = []
        for node, emb in zip(graph.nodes, node_embs):
            score = _cosine_similarity(q_emb, emb)
            scored_nodes.append((node, score))

        scored_nodes.sort(key=lambda x: x[1], reverse=True)

        top_k = self.settings.graph_context_top_k_nodes
        top_nodes = [n for n, _ in scored_nodes[:top_k]]

        if not top_nodes:
            return None

        top_ids = {n.id for n in top_nodes}
        id_to_label = {n.id: n.label for n in graph.nodes}

        # 4) Build textual representation of nodes
        node_lines = [
            f"- {n.label} (type: {n.type}): {n.description or ''}".strip()
            for n in top_nodes
        ]

        # 5) Include edges between those nodes (limited)
        edge_lines: List[str] = []
        max_edges = 15
        for e in graph.edges:
            if e.source in top_ids and e.target in top_ids:
                src = id_to_label.get(e.source, e.source)
                tgt = id_to_label.get(e.target, e.target)
                edge_lines.append(f"- {src} --[{e.relation}]--> {tgt}")
                if len(edge_lines) >= max_edges:
                    break

        # 6) Final graph context block
        parts: List[str] = []
        parts.append("Key entities and concepts from the knowledge graph that may be relevant:")
        parts.append("Nodes:")
        parts.extend(node_lines)

        if edge_lines:
            parts.append("")
            parts.append("Relations between these nodes:")
            parts.extend(edge_lines)

        return "\n".join(parts)
