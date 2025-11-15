import argparse

from ..config import AppConfig
from ..data.loaders import build_chunks_from_pdf
from ..data.synthetic_labels import build_supervision
from ..retrieval.vectordb import ChromaManager
from ..utils.logging import get_logger
from ..utils.io import write_json
import random
import os

logger = get_logger("build_index")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=str, required=True, help="Path to corpus PDF")
    parser.add_argument("--collection", type=str, default=None)
    parser.add_argument("--db_path", type=str, default=None)
    parser.add_argument("--reset", action="store_true", help="Drop and recreate collection")
    args = parser.parse_args()

    cfg = AppConfig()
    if args.collection: cfg.vdb.collection_name = args.collection
    if args.db_path: cfg.vdb.path = args.db_path

    logger.info("Chunking PDF...")
    chunks = build_chunks_from_pdf(args.pdf, cfg.chunks)
    logger.info(f"Total chunks: {len(chunks)}")

    vdb = ChromaManager(cfg.vdb.path, cfg.vdb.collection_name, cfg.vdb.distance)
    if args.reset:
        logger.info("Resetting collection...")
        vdb.reset()

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    vdb.add_documents(chunks, ids)
    logger.info(f"Indexed {len(chunks)} chunks into '{cfg.vdb.collection_name}' at '{cfg.vdb.path}'")

    # train.json/validation.json split generation
    logger.info("Generating synthetic labels...")
    pairs = build_supervision(chunks, questions_per_chunk=cfg.chunks.questions_per_chunk, max_concurrency=cfg.chunks.max_concurrency)

    if cfg.divide.shuffle:
        random.Random(cfg.divide.seed).shuffle(pairs)

    if cfg.divide.max_examples is not None:
        pairs = pairs[:cfg.divide.max_examples]

    split_idx = int(len(pairs) * cfg.divide.train_ratio)
    train_data = pairs[:split_idx]
    val_data = pairs[split_idx:]

    write_json(train_data, cfg.paths.train_json)
    write_json(val_data, cfg.paths.validation_json)


if __name__ == "__main__":
    main()
