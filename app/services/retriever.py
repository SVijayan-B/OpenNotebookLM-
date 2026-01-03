from typing import List, Dict

from app.services.embedder import Embedder
from app.services.vector_store import FAISSVectorStore


class Retriever:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: FAISSVectorStore,
        top_k: int = 5,
        min_score: float = 0.3,
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k
        self.min_score = min_score

    def retrieve(self, query: str) -> List[Dict]:
        # 1. Embed the query
        query_vector = self.embedder.model.encode(
            [query],
            normalize_embeddings=True
        )

        # 2. Search FAISS
        results = self.vector_store.search(
            query_vector=query_vector,
            top_k=self.top_k
        )

        # 3. Filter weak matches
        filtered = [
            r for r in results if r["score"] >= self.min_score
        ]

        return filtered

    @staticmethod
    def build_context(results: List[Dict]) -> str:
        """
        Formats retrieved chunks into LLM-ready context
        """
        context_blocks = []

        for i, r in enumerate(results, start=1):
            source = r["source"]

            if r.get("page") is not None:
                citation = f"{source} (page {r['page']})"
            else:
                citation = (
                    f"{source} "
                    f"[{r.get('start_time', 0):.2f}s - "
                    f"{r.get('end_time', 0):.2f}s]"
                )

            block = (
                f"[Source {i}: {citation}]\n"
                f"{r['content']}"
            )

            context_blocks.append(block)

        return "\n\n".join(context_blocks)
