from app.services.chunker import Chunker
from app.services.embedder import Embedder
from app.services.vector_store import FAISSVectorStore
from app.models.document import DocumentChunk
from app.models.video import VideoSegment
from typing import List, Union


class IngestionPipeline:
    def __init__(self):
        self.chunker = Chunker()
        self.embedder = Embedder(device=None)
        self.vector_store = FAISSVectorStore()

    def ingest_documents(self, docs: List[DocumentChunk]):
        chunks = self.chunker.chunk_documents(docs)
        embeddings = self.embedder.embed_chunks(chunks)
        self.vector_store.add(embeddings, chunks)
        self.vector_store.save()

    def ingest_videos(self, segments: List[VideoSegment]):
        chunks = self.chunker.chunk_video_segments(segments)
        embeddings = self.embedder.embed_chunks(chunks)
        self.vector_store.add(embeddings, chunks)
        self.vector_store.save()
