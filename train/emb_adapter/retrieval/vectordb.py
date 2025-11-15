from typing import List, Sequence
import chromadb

class ChromaManager:
    """
    Simple wrapper for a Chroma collection storing documents (already embedded by Chroma's default sentence-transformers).
    """
    def __init__(self, path: str, collection_name: str, space: str = "cosine"):
        self.client = chromadb.PersistentClient(path=path)
        self.col = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": space}
        )

    def reset(self):
        # Caution: deletes and recreates the collection
        name = self.col.name
        self.client.delete_collection(name)
        self.col = self.client.get_or_create_collection(name=name, metadata=self.col.metadata)

    def add_documents(self, docs: Sequence[str], ids: Sequence[str]) -> None:
        self.col.add(documents=list(docs), ids=list(ids))

    def query_by_embedding(self, emb, k: int = 10) -> List[str]:
        # emb can be numpy array or list; Chroma expects a list of lists
        emb_list = emb.tolist() if hasattr(emb, "tolist") else emb
        if isinstance(emb_list[0], (float, int)):
            emb_list = [emb_list]
        res = self.col.query(query_embeddings=emb_list, n_results=k)
        return res["documents"][0]
