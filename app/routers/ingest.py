import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ingest import IngestRequest, IngestResponse
from app.services.ingestion_service import IngestionService

router = APIRouter(tags=["ingest"])
logger = logging.getLogger(__name__)


@router.post("/ingest", response_model=IngestResponse)
def ingest_document(payload: IngestRequest, db: Session = Depends(get_db)) -> IngestResponse:
    service = IngestionService(db)
    try:
        return service.ingest(title=payload.title, text=payload.text)
    except Exception:
        logger.exception("ingest.failed")
        raise HTTPException(status_code=500, detail="Ingestion failed")