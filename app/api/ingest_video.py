from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path

from app.services.video_loader import VideoLoader

router = APIRouter(prefix="/ingest", tags=["Video Ingestion"])

UPLOAD_DIR = Path("data/videos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

video_loader = VideoLoader(model_size="base")


@router.post("/video")
async def ingest_video(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    segments = video_loader.transcribe(file_path)

    return {
        "filename": file.filename,
        "segments_extracted": len(segments),
        "preview": segments[:2]
    }
