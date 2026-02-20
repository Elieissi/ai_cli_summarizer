from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.init_db import init_db
from app.routers.document import router as document_router
from app.routers.health import router as health_router
from app.routers.ingest import router as ingest_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="AI Summarizer API", version="1.0.0", lifespan=lifespan)

app.include_router(ingest_router)
app.include_router(document_router)
app.include_router(health_router)