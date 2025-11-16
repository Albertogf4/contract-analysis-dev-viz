from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ChunkConfig:
    model_name: str = "gpt-4" # used by tiktoken-based splitter only
    chunk_size: int = 1000
    chunk_overlap: int = 400
    questions_per_chunk: int = 10
    max_concurrency: int = 10 # for API calls

@dataclass
class VectorDBConfig:
    path: str = "./chroma_db"
    collection_name: str = "sf_collection"
    distance: str = "cosine" # hnsw:space

@dataclass
class DivideConfig:
    train_ratio: float = 0.8
    shuffle: bool = True
    seed: int = 42 # RNG seed used for shuffling so that it is reproducible.
    max_examples: Optional[int] = None # useful for debugging or quick experiments

@dataclass
class ModelConfig:
    base_encoder_name: str = "all-MiniLM-L6-v2"  # 384-dim

@dataclass
class TrainConfig:
    num_epochs: int = 10
    batch_size: int = 32
    learning_rate: float = 3e-3
    warmup_steps: int = 100
    max_grad_norm: float = 1.0
    margin: float = 1.0
    seed: int = 42
    device: Optional[str] = None  # "cuda" | "mps" | "cpu" | None -> auto

@dataclass
class EvalConfig:
    k: int = 10

@dataclass
class PathsConfig:
    # Fill with your files
    corpus_pdf: str = "./data/Apple_Environmental_Progress_Report_2024.pdf"
    negatives_pdf: str = "./data/nvidia_10k.pdf"
    train_json: str = "./data/train.json"
    val_json: str = "./data/validation.json"
    adapter_out: str = "./adapters/linear_adapter.pth"

@dataclass
class AppConfig:
    chunks: ChunkConfig = field(default_factory=ChunkConfig)
    vdb: VectorDBConfig = field(default_factory=VectorDBConfig)
    divide: DivideConfig = field(default_factory=DivideConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    eval: EvalConfig = field(default_factory=EvalConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)
