"""Legacy entry module.

Run the API with: uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

from app.main import app

__all__ = ["app"]
