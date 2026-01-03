import subprocess
from pathlib import Path
import whisper
from typing import List

from app.models.video import VideoSegment


class VideoLoader:
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)

    def extract_audio(self, video_path: Path) -> Path:
        audio_path = video_path.with_suffix(".wav")

        command = [
            "ffmpeg",
            "-y",
            "-i", str(video_path),
            "-ac", "1",
            "-ar", "16000",
            str(audio_path)
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return audio_path

    def transcribe(self, video_path: Path) -> List[VideoSegment]:
        audio_path = self.extract_audio(video_path)

        result = self.model.transcribe(
            str(audio_path),
            word_timestamps=False,
            verbose=False
        )

        segments = []
        for seg in result["segments"]:
            segments.append(
                VideoSegment(
                    content=seg["text"].strip(),
                    source=video_path.name,
                    start_time=seg["start"],
                    end_time=seg["end"]
                )
            )

        return segments
