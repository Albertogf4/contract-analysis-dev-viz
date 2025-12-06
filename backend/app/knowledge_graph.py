from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import os
import json

from .config import Settings


@dataclass
class KGNode:
    id: str
    label: str
    type: str
    description: Optional[str] = None


@dataclass
class KGEdge:
    id: str
    source: str
    target: str
    relation: str


@dataclass
class KnowledgeGraph:
    document_id: str
    nodes: List[KGNode]
    edges: List[KGEdge]

    def to_dict(self) -> Dict:
        return {
            "document_id": self.document_id,
            "nodes": [asdict(n) for n in self.nodes],
            "edges": [asdict(e) for e in self.edges],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "KnowledgeGraph":
        nodes = [KGNode(**n) for n in data.get("nodes", [])]
        edges = [KGEdge(**e) for e in data.get("edges", [])]
        return cls(
            document_id=data["document_id"],
            nodes=nodes,
            edges=edges,
        )

    def find_node(self, node_id: str) -> Optional[KGNode]:
        return next((n for n in self.nodes if n.id == node_id), None)


class KnowledgeGraphStore:
    """
    Simple file-based graph store: one JSON file per document.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        os.makedirs(self.settings.graph_dir, exist_ok=True)

    def _graph_path(self, document_id: str) -> str:
        return os.path.join(self.settings.graph_dir, f"{document_id}.json")

    def save_graph(self, graph: KnowledgeGraph) -> None:
        path = self._graph_path(graph.document_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(graph.to_dict(), f, ensure_ascii=False, indent=2)

    def load_graph(self, document_id: str) -> Optional[KnowledgeGraph]:
        path = self._graph_path(document_id)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return KnowledgeGraph.from_dict(data)

    def get_node_and_neighbors(
        self,
        document_id: str,
        node_id: str,
    ) -> Optional[Dict]:
        """
        Returns a small subgraph: the selected node, its 1-hop neighbors and the connecting edges.
        """
        graph = self.load_graph(document_id)
        if graph is None:
            return None

        center = graph.find_node(node_id)
        if center is None:
            return None

        # 1-hop neighbors
        neighbor_ids = set()
        relevant_edges: List[KGEdge] = []
        for e in graph.edges:
            if e.source == node_id or e.target == node_id:
                relevant_edges.append(e)
                neighbor_ids.add(e.source)
                neighbor_ids.add(e.target)

        neighbor_ids.discard(node_id)

        neighbors = [n for n in graph.nodes if n.id in neighbor_ids]

        return {
            "document_id": graph.document_id,
            "center": asdict(center),
            "neighbors": [asdict(n) for n in neighbors],
            "edges": [asdict(e) for e in relevant_edges],
        }
