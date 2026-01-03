from pathlib import Path
from typing import List
from pypdf import PdfReader
import markdown

from app.models.document import DocumentChunk


class DocumentLoader:
    @staticmethod
    def load(file_path: str) -> List[DocumentChunk]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return DocumentLoader._load_pdf(path)
        elif suffix in [".txt", ".md"]:
            return DocumentLoader._load_text(path)
        else:
            raise ValueError("Unsupported file type")

    @staticmethod
    def _load_pdf(path: Path) -> List[DocumentChunk]:
        reader = PdfReader(str(path))
        documents = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                documents.append(
                    DocumentChunk(
                        content=text.strip(),
                        source=path.name,
                        page=i + 1
                    )
                )

        return documents

    @staticmethod
    def _load_text(path: Path) -> List[DocumentChunk]:
        raw_text = path.read_text(encoding="utf-8")

        if path.suffix.lower() == ".md":
            raw_text = markdown.markdown(raw_text)

        return [
            DocumentChunk(
                content=raw_text.strip(),
                source=path.name
            )
        ]
