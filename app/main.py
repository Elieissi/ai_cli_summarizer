from fastapi import FastAPI

from app.db.init_db import init_db
from app.routers.document import router as document_router
from app.routers.ingest import router as ingest_router

app = FastAPI(title="AI Summarizer API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(ingest_router)
app.include_router(document_router)
