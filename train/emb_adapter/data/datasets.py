from typing import List, Dict, Protocol, Tuple
import random
import torch
from torch.utils.data import Dataset

class NegativeSampler(Protocol):
    def sample(self) -> str: ...

class RandomNegativeSampler:
    def __init__(self, negatives: List[str]):
        if not negatives:
            raise ValueError("Negative chunks list is empty")
        self.negatives = negatives

    def sample(self) -> str:
        return random.choice(self.negatives)

class TripletDataset(Dataset):
    """
    Each item is (query_emb, positive_emb, negative_emb)
    Embeddings are computed on-the-fly via the provided encoder.
    """
    def __init__(self,
                 data: List[Dict[str, str]],
                 base_encoder,
                 negative_sampler: NegativeSampler):
        self.data = data
        self.encoder = base_encoder
        self.neg = negative_sampler

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        item = self.data[idx]
        q: str = item["question"]
        p: str = item["chunk"]
        n: str = self.neg.sample()

        q_emb = self.encoder.encode_to_tensor(q)   # torch.Tensor [D]
        p_emb = self.encoder.encode_to_tensor(p)
        n_emb = self.encoder.encode_to_tensor(n)

        return q_emb, p_emb, n_emb
