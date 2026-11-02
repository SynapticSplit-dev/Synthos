from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InputRecord:
    raw_text: str
    normalized_text: str
    tokens: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class InputProcessor:
    """Normalize text, split into tokens, and prepare a safe processing payload."""

    def normalize(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")
        cleaned = text.strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    def tokenize(self, text: str) -> list[str]:
        normalized = self.normalize(text)
        if not normalized:
            return []
        return re.findall(r"\b[\w'-]+\b", normalized.lower())

    def prepare(self, text: str, metadata: dict[str, Any] | None = None) -> InputRecord:
        normalized = self.normalize(text)
        tokens = self.tokenize(normalized)
        record = InputRecord(
            raw_text=text,
            normalized_text=normalized,
            tokens=tokens,
            metadata=metadata or {},
        )
        return record
