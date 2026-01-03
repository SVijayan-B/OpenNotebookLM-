from fastapi import FastAPI
from app.core.config import settings
from app.api import health

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Register routers
app.include_router(health.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to OpenNotebookLM++ API"
    }
