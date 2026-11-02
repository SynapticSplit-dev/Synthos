from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryRecord:
    key: str
    content: str
    memory_type: str
    metadata: dict[str, Any] = field(default_factory=dict)
    ttl: float | None = None
    created_at: float = 0.0


class MemoryStore:
    """Simple in-memory architecture for working, short-term, episodic and semantic memory."""

    def __init__(self, max_entries: int = 256):
        self.max_entries = max_entries
        self.records: list[MemoryRecord] = []

    def add(self, key: str, content: str, memory_type: str, metadata: dict[str, Any] | None = None, ttl: float | None = None) -> MemoryRecord:
        record = MemoryRecord(
            key=key,
            content=content,
            memory_type=memory_type,
            metadata=metadata or {},
            ttl=ttl,
            created_at=__import__("time").time(),
        )
        self.records.append(record)
        if len(self.records) > self.max_entries:
            self.records.pop(0)
        return record

    def get(self, key: str | None = None, memory_type: str | None = None) -> list[MemoryRecord]:
        results = []
        for record in self.records:
            if key is not None and record.key != key:
                continue
            if memory_type is not None and record.memory_type != memory_type:
                continue
            results.append(record)
        return results

    def search(self, query: str, limit: int = 5) -> list[MemoryRecord]:
        query_tokens = set(query.lower().split())
        scored = []
        for record in self.records:
            tokens = set(record.content.lower().split())
            overlap = len(query_tokens & tokens)
            if overlap > 0:
                scored.append((overlap, record))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in scored[:limit]]

    def update(self, key: str, content: str, memory_type: str, metadata: dict[str, Any] | None = None) -> MemoryRecord | None:
        for record in self.records:
            if record.key == key:
                record.content = content
                record.memory_type = memory_type
                if metadata is not None:
                    record.metadata = metadata
                return record
        return None

    def expire(self) -> list[MemoryRecord]:
        now = __import__("time").time()
        expired = []
        remaining = []
        for record in self.records:
            if record.ttl is not None and (now - record.created_at) > record.ttl:
                expired.append(record)
            else:
                remaining.append(record)
        self.records = remaining
        return expired

    def reconstruct_context(self, limit: int = 10) -> str:
        entries = self.records[-limit:]
        return " ".join(item.content for item in entries if item.content)

    def stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        for record in self.records:
            by_type[record.memory_type] = by_type.get(record.memory_type, 0) + 1
        return {"entries": len(self.records), "by_type": by_type}
