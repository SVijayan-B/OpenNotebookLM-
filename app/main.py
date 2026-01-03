from fastapi import FastAPI

from app.core.config import settings
from app.api import health, ingest, ingest_video

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Register routers
app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(ingest_video.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to OpenNotebookLM++ API"
    }
