import os


class ChunkingService:
    def __init__(self) -> None:
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1200"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
        if self.chunk_size <= 0:
            raise ValueError("CHUNK_SIZE must be greater than 0")
        if self.chunk_overlap < 0 or self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must satisfy 0 <= overlap < chunk_size")

    def chunk_text(self, text: str) -> list[str]:
        normalized = text.strip()
        if not normalized:
            return []

        chunks: list[str] = []
        start = 0
        step = self.chunk_size - self.chunk_overlap
        while start < len(normalized):
            end = min(start + self.chunk_size, len(normalized))
            chunk = normalized[start:end]
            chunks.append(chunk)
            if end == len(normalized):
                break
            start += step
        return chunks
