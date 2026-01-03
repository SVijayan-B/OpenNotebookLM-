import faiss
import numpy as np
from pathlib import Path
from typing import List

from app.models.chunk import TextChunk


class FAISSVectorStore:
    def __init__(self, dim: int = 384, index_path: str = "data/faiss.index"):
        self.dim = dim
        self.index_path = Path(index_path)
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: List[TextChunk] = []

        if self.index_path.exists():
            self._load()

    def add(self, embeddings: np.ndarray, chunks: List[TextChunk]):
        if embeddings.shape[0] != len(chunks):
            raise ValueError("Embeddings and chunks length mismatch")

        self.index.add(embeddings)
        self.metadata.extend(chunks)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue

            chunk = self.metadata[idx]
            results.append(
                {
                    "content": chunk.content,
                    "source": chunk.source,
                    "page": chunk.page,
                    "start_time": chunk.start_time,
                    "end_time": chunk.end_time,
                    "score": float(score),
                }
            )

        return results

    def save(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))

        meta_path = self.index_path.with_suffix(".meta.npy")
        np.save(meta_path, self.metadata, allow_pickle=True)

    def _load(self):
        self.index = faiss.read_index(str(self.index_path))

        meta_path = self.index_path.with_suffix(".meta.npy")
        if meta_path.exists():
            self.metadata = list(np.load(meta_path, allow_pickle=True))
