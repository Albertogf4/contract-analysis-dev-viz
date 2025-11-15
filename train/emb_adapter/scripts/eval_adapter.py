import argparse
from ..config import AppConfig
from ..utils.io import read_json, validate_supervision_schema
from ..utils.logging import get_logger

from ..models.base_encoder import BaseEncoder
from ..models.linear_adapter import LinearAdapter
from ..retrieval.vectordb import ChromaManager
from ..retrieval.evaluator import QueryEncoder, Evaluator

logger = get_logger("eval_adapter")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--val_json", type=str, help="Path to validation.json")
    parser.add_argument("--db_path", type=str, help="Chroma path")
    parser.add_argument("--collection", type=str, help="Collection name")
    parser.add_argument("--k", type=int, help="Recall@k / MRR@k")
    parser.add_argument("--adapter", type=str, default=None, help="Path to adapter .pth (optional)")
    parser.add_argument("--device", type=str, default=None)
    args = parser.parse_args()

    cfg = AppConfig()
    if args.val_json: cfg.paths.val_json = args.val_json
    if args.db_path: cfg.vdb.path = args.db_path
    if args.collection: cfg.vdb.collection_name = args.collection
    if args.k is not None: cfg.eval.k = args.k

    logger.info("Loading validation data...")
    val_data = read_json(cfg.paths.val_json)
    validate_supervision_schema(val_data)
    logger.info(f"Validation pairs: {len(val_data)}")

    logger.info("Loading VDB...")
    vdb = ChromaManager(cfg.vdb.path, cfg.vdb.collection_name, cfg.vdb.distance)

    logger.info("Loading base encoder...")
    base = BaseEncoder(cfg.model.base_encoder_name)

    adapter = None
    if args.adapter:
        logger.info(f"Loading adapter from {args.adapter}")
        adapter, meta = LinearAdapter.load(args.adapter, base.sentence_embedding_dim())
        logger.info(f"Adapter hyperparams: {meta}")

    qe = QueryEncoder(base_encoder=base, adapter=adapter, device=args.device)
    evaluator = Evaluator(vdb=vdb, query_encoder=qe, k=cg.eval.k if (cg:=cfg) else cfg.eval.k)

    res = evaluator.evaluate(val_data)
    logger.info(f"Average Hit Rate @ {cfg.eval.k}: {res['average_hit_rate']:.6f}")
    logger.info(f"Mean Reciprocal Rank @ {cfg.eval.k}: {res['average_reciprocal_rank']:.6f}")

    print(f"Average Hit Rate @{cfg.eval.k}: {res['average_hit_rate']}")
    print(f"Mean Reciprocal Rank @{cfg.eval.k}: {res['average_reciprocal_rank']}")

if __name__ == "__main__":
    main()
