import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.main import app
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.processing_result import ProcessingResult


@pytest.fixture(autouse=True)
def clean_db() -> None:
    init_db()
    db = SessionLocal()
    try:
        db.query(Chunk).delete()
        db.query(ProcessingResult).delete()
        db.query(Document).delete()
        db.commit()
    finally:
        db.close()
    yield
    db = SessionLocal()
    try:
        db.query(Chunk).delete()
        db.query(ProcessingResult).delete()
        db.query(Document).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
