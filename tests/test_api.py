from app.db.session import DATABASE_URL
from app.services import ingestion_service
from app.services.openai_service import UsageTotals


class FakeOpenAIService:
    def summarize_chunk(self, chunk_text: str):
        return f"summary:{chunk_text[:20]}", UsageTotals(prompt_tokens=10, completion_tokens=5)

    def combine_summaries(self, chunk_summaries: list[str]):
        return "final-summary", UsageTotals(prompt_tokens=3, completion_tokens=2)


def test_database_url_isolated_for_tests() -> None:
    assert DATABASE_URL.endswith("tests/test_app.db")


def test_ingest_and_get_document_happy_path(client, monkeypatch) -> None:
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


def test_ingest_internal_errors_are_sanitized(client, monkeypatch) -> None:
    class BrokenOpenAIService:
        def summarize_chunk(self, chunk_text: str):
            raise RuntimeError("secret failure details")

        def combine_summaries(self, chunk_summaries: list[str]):
            return "unused", UsageTotals(prompt_tokens=0, completion_tokens=0)

    monkeypatch.setattr(ingestion_service, "OpenAIService", BrokenOpenAIService)

    response = client.post(
        "/ingest",
        json={"title": "Doc", "text": "A test body that triggers a failure."},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Ingestion failed"


def test_health_endpoint_returns_ok(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["db"] == "ok"