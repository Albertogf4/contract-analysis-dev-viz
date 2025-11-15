from typing import Dict, Any
import torch
from torch import nn

class LinearAdapter(nn.Module):
    """
    Query-only linear adapter: R^D -> R^D
    """
    def __init__(self, input_dim: int):
        super().__init__()
        self.linear = nn.Linear(input_dim, input_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x)

    @staticmethod
    def save(adapter: "LinearAdapter", path: str, adapter_kwargs: Dict[str, Any]) -> None:
        payload = {
            "adapter_state_dict": adapter.state_dict(),
            "adapter_kwargs": adapter_kwargs,
        }
        torch.save(payload, path)

    @staticmethod
    def load(path: str, input_dim: int) -> "LinearAdapter":
        payload = torch.load(path, map_location="cpu")
        adapter = LinearAdapter(input_dim)
        adapter.load_state_dict(payload["adapter_state_dict"])
        return adapter, payload.get("adapter_kwargs", {})
