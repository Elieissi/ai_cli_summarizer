from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.document import DocumentResponse
from app.services.ingestion_service import IngestionService

router = APIRouter(tags=["document"])


@router.get("/document/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)) -> DocumentResponse:
    service = IngestionService(db)
    response = service.get_document(document_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return response
