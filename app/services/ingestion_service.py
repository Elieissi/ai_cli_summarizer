import json
import time
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import Document
from app.models.processing_result import ProcessingResult
from app.schemas.common import ChunkSummary
from app.schemas.document import DocumentResponse
from app.schemas.ingest import IngestResponse
from app.services.chunking import ChunkingService
from app.services.openai_service import OpenAIService, UsageTotals


class IngestionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.chunking_service = ChunkingService()

    def ingest(self, title: str | None, text: str) -> IngestResponse:
        started = time.perf_counter()
        openai_service = OpenAIService()

        document = Document(
            title=title or "Untitled Document",
            status="pending",
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        if not title:
            document.title = f"Document {document.id}"
            self.db.commit()
            self.db.refresh(document)

        try:
            chunks = self.chunking_service.chunk_text(text)
            chunk_models: list[Chunk] = []
            chunk_summaries: list[ChunkSummary] = []
            intermediate_summaries: list[str] = []
            usage_totals = UsageTotals()

            for idx, chunk_text in enumerate(chunks):
                chunk_model = Chunk(document_id=document.id, chunk_index=idx, content=chunk_text)
                self.db.add(chunk_model)
                self.db.flush()

                summary, usage = openai_service.summarize_chunk(chunk_text)
                chunk_model.summary = summary
                chunk_models.append(chunk_model)

                chunk_summaries.append(
                    ChunkSummary(chunk_index=idx, chunk_text=chunk_text, summary=summary)
                )
                intermediate_summaries.append(summary)
                usage_totals.prompt_tokens += usage.prompt_tokens
                usage_totals.completion_tokens += usage.completion_tokens

            final_summary, final_usage = openai_service.combine_summaries(intermediate_summaries)
            usage_totals.prompt_tokens += final_usage.prompt_tokens
            usage_totals.completion_tokens += final_usage.completion_tokens

            response_payload = {
                "document_id": document.id,
                "title": document.title,
                "status": "completed",
                "final_summary": final_summary,
                "chunk_summaries": [item.model_dump() for item in chunk_summaries],
                "token_usage_prompt": usage_totals.prompt_tokens,
                "token_usage_completion": usage_totals.completion_tokens,
                "processing_duration_ms": int((time.perf_counter() - started) * 1000),
                "created_at": document.created_at,
            }

            result = ProcessingResult(
                document_id=document.id,
                final_summary=final_summary,
                raw_output_json=json.dumps(response_payload, default=str),
            )
            self.db.add(result)

            document.status = "completed"
            document.processing_duration_ms = response_payload["processing_duration_ms"]
            document.token_usage_prompt = usage_totals.prompt_tokens
            document.token_usage_completion = usage_totals.completion_tokens
            document.error_message = None

            self.db.commit()
            self.db.refresh(document)

            return IngestResponse(**response_payload)

        except Exception as exc:
            document.status = "failed"
            document.processing_duration_ms = int((time.perf_counter() - started) * 1000)
            document.error_message = str(exc)
            self.db.commit()
            raise

    def get_document(self, document_id: int) -> DocumentResponse | None:
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if document is None:
            return None

        chunk_rows = (
            self.db.query(Chunk)
            .filter(Chunk.document_id == document.id)
            .order_by(Chunk.chunk_index.asc())
            .all()
        )
        result_row = (
            self.db.query(ProcessingResult)
            .filter(ProcessingResult.document_id == document.id)
            .first()
        )

        return DocumentResponse(
            document_id=document.id,
            title=document.title,
            status=document.status,
            final_summary=result_row.final_summary if result_row else None,
            chunk_summaries=[
                ChunkSummary(
                    chunk_index=row.chunk_index,
                    chunk_text=row.content,
                    summary=row.summary or "",
                )
                for row in chunk_rows
            ],
            token_usage_prompt=document.token_usage_prompt,
            token_usage_completion=document.token_usage_completion,
            processing_duration_ms=document.processing_duration_ms,
            created_at=document.created_at,
        )
