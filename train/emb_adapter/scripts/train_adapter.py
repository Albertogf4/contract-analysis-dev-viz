import argparse
from ..config import AppConfig
from ..utils.io import read_json, validate_supervision_schema
from ..utils.seed import set_seed
from ..utils.logging import get_logger

from ..models.base_encoder import BaseEncoder
from ..models.linear_adapter import LinearAdapter

from ..data.loaders import build_chunks_from_pdf
from ..data.datasets import TripletDataset, RandomNegativeSampler

from ..training.trainer import Trainer

logger = get_logger("train_adapter")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_json", type=str, help="Path to train.json")
    parser.add_argument("--negatives_pdf", type=str, help="Path to negatives PDF")
    parser.add_argument("--out", type=str, help="Path to save adapter .pth")
    parser.add_argument("--epochs", type=int)
    parser.add_argument("--batch_size", type=int)
    parser.add_argument("--lr", type=float)
    parser.add_argument("--warmup", type=int)
    parser.add_argument("--margin", type=float)
    parser.add_argument("--max_grad_norm", type=float)
    parser.add_argument("--device", type=str, default=None, help="cuda|mps|cpu|None")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    cfg = AppConfig()
    if args.train_json: cfg.paths.train_json = args.train_json
    if args.negatives_pdf: cfg.paths.negatives_pdf = args.negatives_pdf
    if args.out: cfg.paths.adapter_out = args.out

    if args.epochs is not None: cfg.train.num_epochs = args.epochs
    if args.batch_size is not None: cfg.train.batch_size = args.batch_size
    if args.lr is not None: cfg.train.learning_rate = args.lr
    if args.warmup is not None: cfg.train.warmup_steps = args.warmup
    if args.margin is not None: cfg.train.margin = args.margin
    if args.max_grad_norm is not None: cfg.train.max_grad_norm = args.max_grad_norm
    if args.device is not None: cfg.train.device = args.device
    if args.seed is not None: cfg.train.seed = args.seed

    set_seed(cfg.train.seed)

    logger.info("Loading supervision...")
    train_data = read_json(cfg.paths.train_json)
    validate_supervision_schema(train_data)
    logger.info(f"Train pairs: {len(train_data)}")

    logger.info("Preparing negatives...")
    negative_chunks = build_chunks_from_pdf(cfg.paths.negatives_pdf, cfg.chunks)
    neg_sampler = RandomNegativeSampler(negative_chunks)

    logger.info("Loading base encoder...")
    base = BaseEncoder(cfg.model.base_encoder_name)

    logger.info("Creating dataset...")
    dataset = TripletDataset(train_data, base, neg_sampler)

    logger.info("Building adapter and trainer...")
    adapter = LinearAdapter(base.sentence_embedding_dim())

    trainer = Trainer(
        adapter=adapter,
        dataset=dataset,
        learning_rate=cfg.train.learning_rate,
        batch_size=cfg.train.batch_size,
        warmup_steps=cfg.train.warmup_steps,
        max_grad_norm=cfg.train.max_grad_norm,
        margin=cfg.train.margin,
        device=cfg.train.device
    )

    logger.info("Starting training...")
    trainer.train(cfg.train.num_epochs)

    logger.info(f"Saving adapter to {cfg.paths.adapter_out}")
    LinearAdapter.save(
        trainer.adapter,
        cfg.paths.adapter_out,
        adapter_kwargs=dict(
            num_epochs=cfg.train.num_epochs,
            batch_size=cfg.train.batch_size,
            learning_rate=cfg.train.learning_rate,
            warmup_steps=cfg.train.warmup_steps,
            max_grad_norm=cfg.train.max_grad_norm,
            margin=cfg.train.margin
        )
    )
    logger.info("Done.")

if __name__ == "__main__":
    main()
