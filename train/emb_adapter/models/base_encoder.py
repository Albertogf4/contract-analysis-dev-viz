from typing import List, Union
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

class BaseEncoder:
    """
    Thin wrapper around SentenceTransformer that provides both numpy and tensor encodings.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode_to_numpy(self, text: Union[str, List[str]]) -> np.ndarray:
        return self.model.encode(text)

    def encode_to_tensor(self, text: Union[str, List[str]]) -> torch.Tensor:
        return self.model.encode(text, convert_to_tensor=True)

    def sentence_embedding_dim(self) -> int:
        return self.dim
