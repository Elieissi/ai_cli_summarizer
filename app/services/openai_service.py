import os
import time
from dataclasses import dataclass

from openai import OpenAI, OpenAIError


@dataclass
class UsageTotals:
    prompt_tokens: int = 0
    completion_tokens: int = 0


class OpenAIService:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")

        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "3"))
        self.retry_base_seconds = float(os.getenv("OPENAI_RETRY_BASE_SECONDS", "1.0"))
        self.client = OpenAI(api_key=api_key)

    def summarize_chunk(self, chunk_text: str) -> tuple[str, UsageTotals]:
        response = self._with_retry(
            [
                {"role": "system", "content": "You summarize text clearly and concisely."},
                {"role": "user", "content": f"Summarize this text:\n\n{chunk_text}"},
            ]
        )
        summary = (response.choices[0].message.content or "").strip()
        usage = self._usage_from_response(response)
        return summary, usage

    def combine_summaries(self, chunk_summaries: list[str]) -> tuple[str, UsageTotals]:
        joined = "\n\n".join(
            f"Chunk {idx + 1}:\n{text}" for idx, text in enumerate(chunk_summaries)
        )
        response = self._with_retry(
            [
                {
                    "role": "system",
                    "content": "You combine chunk summaries into one coherent final summary.",
                },
                {
                    "role": "user",
                    "content": f"Combine these chunk summaries into one final summary:\n\n{joined}",
                },
            ]
        )
        final_summary = (response.choices[0].message.content or "").strip()
        usage = self._usage_from_response(response)
        return final_summary, usage

    def _with_retry(self, messages: list[dict[str, str]]):
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.4,
                )
            except OpenAIError as exc:
                last_error = exc
                if attempt == self.max_retries - 1:
                    break
                delay = self.retry_base_seconds * (2**attempt)
                time.sleep(delay)
        raise RuntimeError(f"OpenAI request failed after retries: {last_error}")

    @staticmethod
    def _usage_from_response(response) -> UsageTotals:
        usage = getattr(response, "usage", None)
        if not usage:
            return UsageTotals()
        return UsageTotals(
            prompt_tokens=int(getattr(usage, "prompt_tokens", 0) or 0),
            completion_tokens=int(getattr(usage, "completion_tokens", 0) or 0),
        )
