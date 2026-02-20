from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProcessingResult(Base):
    __tablename__ = "processing_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    final_summary: Mapped[str] = mapped_column(Text, nullable=False)
    raw_output_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    document = relationship("Document", back_populates="processing_result")
