"""Legacy module retained for compatibility.

OpenAI orchestration now lives in app/services/openai_service.py.
"""


class Summarizer:
    def __init__(self, *_args, **_kwargs) -> None:
        raise RuntimeError("Summarizer is deprecated. Use FastAPI endpoints instead.")
