# AI Summarizer FastAPI Service

This project is a containerized FastAPI backend that ingests raw text, chunks it, summarizes each chunk with OpenAI, and stores all results in SQLite via SQLAlchemy.

## Project Structure

```text
app/
  main.py
  routers/
  services/
  models/
  schemas/
  db/
```

## Setup (Local)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure environment:

```bash
copy .env.example .env
```

3. Start API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /ingest

Request body:

```json
{
  "title": "My Document",
  "text": "Long text to summarize..."
}
```

Response includes:
- document metadata
- chunk summaries
- final summary
- status, duration, and token usage

### GET /document/{id}

Returns stored document metadata and summaries for a previously ingested document.

## Tests

Run:

```bash
pytest -q
```

Covers:
- `POST /ingest` happy path
- `GET /document/{id}` happy path
- `GET /document/{id}` 404
- `POST /ingest` 422 validation

## Docker

1. Build and run:

```bash
docker compose up --build
```

2. API available at:

`http://localhost:8000`

## Notes

- `OPENAI_API_KEY` is required for real OpenAI processing.
- Processing is synchronous in `POST /ingest`.
- SQLite is used for persistence (`DATABASE_URL`, default `sqlite:///./app.db`).
