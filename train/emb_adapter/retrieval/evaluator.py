from typing import List, Dict, Optional, Protocol
import numpy as np

class EncoderLike(Protocol):
    def encode_to_numpy(self, text: str): ...
    def encode_to_tensor(self, text: str): ...
    def sentence_embedding_dim(self) -> int: ...

class QueryEncoder:
    """
    Wraps the base encoder + optional adapter.
    """
    def __init__(self, base_encoder: EncoderLike, adapter=None, device: Optional[str] = None):
        self.base = base_encoder
        self.adapter = adapter
        self.device = device

    def encode_query_numpy(self, query: str):
        if self.adapter is None:
            return self.base.encode_to_numpy(query)
        import torch
        dev = torch.device(self.device) if self.device else (
            torch.device("cuda") if torch.cuda.is_available() else
            (torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu"))
        )
        with torch.no_grad():
            q = self.base.encode_to_tensor(query).to(dev)
            out = self.adapter(q)
            return out.detach().cpu().numpy()

def reciprocal_rank(retrieved_docs: List[str], ground_truth: str, k: int) -> float:
    try:
        rank = retrieved_docs.index(ground_truth) + 1
        return 1.0 / rank if rank <= k else 0.0
    except ValueError:
        return 0.0

def hit_rate(retrieved_docs: List[str], ground_truth: str, k: int) -> float:
    return 1.0 if ground_truth in retrieved_docs[:k] else 0.0

class Evaluator:
    def __init__(self, vdb, query_encoder: QueryEncoder, k: int = 10):
        self.vdb = vdb
        self.encoder = query_encoder
        self.k = k

    def evaluate(self, validation_data: List[Dict[str, str]]) -> Dict[str, float]:
        hit_rates, rrs = [], []
        for row in validation_data:
            q = row["question"]
            gt = row["chunk"]
            q_emb = self.encoder.encode_query_numpy(q)
            docs = self.vdb.query_by_embedding(q_emb, k=self.k)
            hit_rates.append(hit_rate(docs, gt, self.k))
            rrs.append(reciprocal_rank(docs, gt, self.k))
        return {
            "average_hit_rate": float(np.mean(hit_rates)),
            "average_reciprocal_rank": float(np.mean(rrs)),
        }
