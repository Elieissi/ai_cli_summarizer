"""Legacy module retained for compatibility.

Persistence is now managed by SQLAlchemy models in app/models.
"""


class NoteManager:
    def __init__(self) -> None:
        raise RuntimeError("NoteManager is deprecated. Use FastAPI endpoints instead.")
