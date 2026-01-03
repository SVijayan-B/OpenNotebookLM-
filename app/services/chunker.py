from typing import List
import textwrap

from app.models.document import DocumentChunk
from app.models.video import VideoSegment
from app.models.chunk import TextChunk


class Chunker:
    def __init__(self, max_words: int = 400, overlap_words: int = 80):
        self.max_words = max_words
        self.overlap_words = overlap_words

    # --------------------
    # Document chunking
    # --------------------
    def chunk_documents(self, docs: List[DocumentChunk]) -> List[TextChunk]:
        chunks: List[TextChunk] = []

        for doc in docs:
            words = doc.content.split()
            start = 0

            while start < len(words):
                end = start + self.max_words
                chunk_words = words[start:end]
                content = " ".join(chunk_words)

                chunks.append(
                    TextChunk(
                        content=content,
                        source=doc.source,
                        page=doc.page
                    )
                )

                start = end - self.overlap_words

        return chunks

    # --------------------
    # Video chunking
    # --------------------
    def chunk_video_segments(
        self, segments: List[VideoSegment]
    ) -> List[TextChunk]:
        chunks: List[TextChunk] = []

        buffer_text = []
        buffer_start = None
        buffer_end = None
        word_count = 0

        for seg in segments:
            seg_words = seg.content.split()

            if buffer_start is None:
                buffer_start = seg.start_time

            buffer_text.extend(seg_words)
            buffer_end = seg.end_time
            word_count += len(seg_words)

            if word_count >= self.max_words:
                chunks.append(
                    TextChunk(
                        content=" ".join(buffer_text),
                        source=seg.source,
                        start_time=buffer_start,
                        end_time=buffer_end
                    )
                )

                # overlap handling (10 sec overlap)
                buffer_text = buffer_text[-int(self.overlap_words):]
                word_count = len(buffer_text)
                buffer_start = max(
                    0.0, buffer_end - 10.0
                )

        if buffer_text:
            chunks.append(
                TextChunk(
                    content=" ".join(buffer_text),
                    source=segments[0].source,
                    start_time=buffer_start,
                    end_time=buffer_end
                )
            )

        return chunks
