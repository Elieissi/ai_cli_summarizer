import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import close_all_sessions

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TEST_DB_PATH = Path(__file__).resolve().parent / "test_app.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"

from app.db.init_db import init_db
from app.db.session import SessionLocal, engine
from app.main import app
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.processing_result import ProcessingResult


@pytest.fixture(scope="session", autouse=True)
def ensure_test_database() -> None:
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    init_db()
    yield
    close_all_sessions()
    engine.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest.fixture(autouse=True)
def clean_db() -> None:
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