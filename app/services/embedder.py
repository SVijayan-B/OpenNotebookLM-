from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from app.models.chunk import TextChunk


class Embedder:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: str | None = None
    ):
        """
        device: 'cuda' | 'cpu' | None (auto-detect)
        """
        self.model = SentenceTransformer(model_name, device=device)

    def embed_chunks(self, chunks: List[TextChunk]) -> np.ndarray:
        texts = [chunk.content for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        return embeddings
