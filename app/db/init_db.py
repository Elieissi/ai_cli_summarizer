from app.db.base import Base
from app.db.session import engine
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.processing_result import ProcessingResult


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
