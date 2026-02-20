from pydantic import BaseModel, Field, field_validator

from app.schemas.common import BaseDocumentResponse


class IngestRequest(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    text: str = Field(..., min_length=1)

    @field_validator("text")
    @classmethod
    def text_must_have_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must include non-whitespace characters")
        return value


class IngestResponse(BaseDocumentResponse):
    pass
