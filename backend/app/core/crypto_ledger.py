import hashlib
import json
import unicodedata
from typing import Any


def canonicalize_and_hash_json(payload: dict[str, Any]) -> str:
    """Recursively normalizes strings with NFKC, serializes deterministically,
    and returns SHA-256 hex digest."""
    normalized = _normalize_value(payload)
    serialized = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _normalize_value(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFKC", value)
    elif isinstance(value, dict):
        return {k: _normalize_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_normalize_value(item) for item in value]
    return value


def compute_event_hash(
    prev_hash: str,
    sequence_num: int,
    org_id: str,
    agent_id: str,
    tool_name: str,
    arguments_sha256: str,
    decision: str,
    created_at_iso: str,
) -> str:
    """Compute SHA-256 hash of pipe-delimited event data."""
    data = "|".join([
        prev_hash,
        str(sequence_num),
        str(org_id),
        str(agent_id),
        tool_name,
        arguments_sha256,
        decision,
        created_at_iso,
    ])
    return hashlib.sha256(data.encode("utf-8")).hexdigest()