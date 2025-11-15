from typing import Dict, Any, Optional, List
import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import AdamW
from torch.nn.utils import clip_grad_norm_
from tqdm import tqdm

from ..utils.logging import get_logger
from .scheduler import get_linear_schedule_with_warmup

logger = get_logger("Trainer")

class Trainer:
    """
    Trains a query-only linear adapter on triplet loss with random negatives.
    """
    def __init__(self,
                 adapter,
                 dataset,
                 learning_rate: float = 3e-3,
                 batch_size: int = 32,
                 warmup_steps: int = 100,
                 max_grad_norm: float = 1.0,
                 margin: float = 1.0,
                 device: Optional[str] = None):
        self.adapter = adapter
        self.dataset = dataset
        self.lr = learning_rate
        self.bs = batch_size
        self.warmup = warmup_steps
        self.max_grad_norm = max_grad_norm
        self.margin = margin

        self.triplet_loss = nn.TripletMarginLoss(margin=self.margin, p=2)

        if device is not None:
            self.device = torch.device(device)
        else:
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                self.device = torch.device("mps")
            else:
                self.device = torch.device("cpu")

        self.adapter.to(self.device)

    def train(self, num_epochs: int = 10) -> None:
        optimizer = AdamW(self.adapter.parameters(), lr=self.lr)
        loader = DataLoader(self.dataset, batch_size=self.bs, shuffle=True)
        total_steps = len(loader) * num_epochs
        scheduler = get_linear_schedule_with_warmup(optimizer, self.warmup, total_steps)

        for epoch in range(1, num_epochs + 1):
            self.adapter.train()
            total_loss = 0.0
            for q, p, n in tqdm(loader, desc=f"Epoch {epoch}/{num_epochs}"):
                q = q.to(self.device)
                p = p.to(self.device)
                n = n.to(self.device)

                optimizer.zero_grad(set_to_none=True)

                q_adapted = self.adapter(q)
                loss = self.triplet_loss(q_adapted, p, n)

                loss.backward()
                clip_grad_norm_(self.adapter.parameters(), self.max_grad_norm)
                optimizer.step()
                scheduler.step()

                total_loss += loss.item()

            avg = total_loss / max(len(loader), 1)
            logger.info(f"Epoch {epoch}/{num_epochs} - Loss: {avg:.4f}")

    @staticmethod
    def train_and_return(adapter, dataset, **kwargs):
        trainer = Trainer(adapter, dataset, **kwargs)
        trainer.train(kwargs.get("num_epochs", 10))
        return trainer.adapter
