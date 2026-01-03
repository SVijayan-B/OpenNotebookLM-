from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path

from app.services.document_loader import DocumentLoader

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/document")
async def ingest_document(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    documents = DocumentLoader.load(str(file_path))

    return {
        "filename": file.filename,
        "chunks_extracted": len(documents),
        "preview": documents[:2]
    }
