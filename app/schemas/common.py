from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ChunkSummary(BaseModel):
    chunk_index: int
    chunk_text: str
    summary: str


class BaseDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: int
    title: str
    status: Literal["pending", "completed", "failed"]
    final_summary: str | None
    chunk_summaries: list[ChunkSummary]
    token_usage_prompt: int | None
    token_usage_completion: int | None
    processing_duration_ms: int | None
    created_at: datetime
