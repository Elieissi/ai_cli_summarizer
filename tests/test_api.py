from app.services import ingestion_service
from app.services.openai_service import UsageTotals


def test_ingest_and_get_document_happy_path(client, monkeypatch) -> None:
    class FakeOpenAIService:
        def summarize_chunk(self, chunk_text: str):
            return f"summary:{chunk_text[:20]}", UsageTotals(prompt_tokens=10, completion_tokens=5)

        def combine_summaries(self, chunk_summaries: list[str]):
            return "final-summary", UsageTotals(prompt_tokens=3, completion_tokens=2)

    monkeypatch.setattr(ingestion_service, "OpenAIService", FakeOpenAIService)

    ingest_payload = {
        "title": "Test Doc",
        "text": "This is a test document body that should be chunked and summarized.",
    }
    ingest_resp = client.post("/ingest", json=ingest_payload)

    assert ingest_resp.status_code == 200
    body = ingest_resp.json()
    assert body["status"] == "completed"
    assert body["title"] == "Test Doc"
    assert body["final_summary"] == "final-summary"
    assert len(body["chunk_summaries"]) >= 1
    assert body["token_usage_prompt"] == 13
    assert body["token_usage_completion"] == 7

    doc_id = body["document_id"]
    get_resp = client.get(f"/document/{doc_id}")

    assert get_resp.status_code == 200
    get_body = get_resp.json()
    assert get_body["document_id"] == doc_id
    assert get_body["status"] == "completed"
    assert get_body["final_summary"] == "final-summary"
    assert len(get_body["chunk_summaries"]) >= 1


def test_get_document_not_found(client) -> None:
    response = client.get("/document/999999")
    assert response.status_code == 404


def test_ingest_validation_error_for_whitespace_text(client) -> None:
    response = client.post("/ingest", json={"title": "Bad", "text": "   "})
    assert response.status_code == 422
