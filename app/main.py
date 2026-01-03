from fastapi import FastAPI
from app.core.config import settings
from app.api import health, ingest

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

app.include_router(health.router)
app.include_router(ingest.router)


@app.get("/")
def root():
    return {"message": "Welcome to OpenNotebookLM++ API"}
