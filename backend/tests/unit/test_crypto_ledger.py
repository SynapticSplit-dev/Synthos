import pytest

from app.core.crypto_ledger import canonicalize_and_hash_json, compute_event_hash


class TestCanonicalizeAndHashJson:
    def test_key_order_independence(self):
        payload1 = {"a": 1, "b": 2}
        payload2 = {"b": 2, "a": 1}
        hash1 = canonicalize_and_hash_json(payload1)
        hash2 = canonicalize_and_hash_json(payload2)
        assert hash1 == hash2

    def test_unicode_nfkc_normalization(self):
        # NFKC normalization: full-width characters should be normalized
        payload1 = {"name": "ｔｅｓｔ"}  # full-width ASCII
        payload2 = {"name": "test"}  # normal ASCII
        hash1 = canonicalize_and_hash_json(payload1)
        hash2 = canonicalize_and_hash_json(payload2)
        assert hash1 == hash2

    def test_nested_structures(self):
        payload1 = {"a": {"b": [1, 2, {"c": "ｘｙｚ"}]}}
        payload2 = {"a": {"b": [1, 2, {"c": "xyz"}]}}
        hash1 = canonicalize_and_hash_json(payload1)
        hash2 = canonicalize_and_hash_json(payload2)
        assert hash1 == hash2

    def test_different_payloads_different_hashes(self):
        hash1 = canonicalize_and_hash_json({"a": 1})
        hash2 = canonicalize_and_hash_json({"a": 2})
        assert hash1 != hash2

    def test_hash_is_64_hex_chars(self):
        result = canonicalize_and_hash_json({"test": "data"})
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)


class TestComputeEventHash:
    def test_hash_is_deterministic(self):
        hash1 = compute_event_hash(
            prev_hash="0" * 64,
            sequence_num=1,
            org_id="org-123",
            agent_id="agent-456",
            tool_name="test_tool",
            arguments_sha256="abc123",
            decision="ALLOWED",
            created_at_iso="2024-01-01T00:00:00+00:00",
        )
        hash2 = compute_event_hash(
            prev_hash="0" * 64,
            sequence_num=1,
            org_id="org-123",
            agent_id="agent-456",
            tool_name="test_tool",
            arguments_sha256="abc123",
            decision="ALLOWED",
            created_at_iso="2024-01-01T00:00:00+00:00",
        )
        assert hash1 == hash2

    def test_hash_is_64_hex_chars(self):
        result = compute_event_hash(
            prev_hash="0" * 64,
            sequence_num=1,
            org_id="org-123",
            agent_id="agent-456",
            tool_name="test_tool",
            arguments_sha256="abc123",
            decision="ALLOWED",
            created_at_iso="2024-01-01T00:00:00+00:00",
        )
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)

    def test_different_inputs_different_hashes(self):
        hash1 = compute_event_hash(
            prev_hash="0" * 64,
            sequence_num=1,
            org_id="org-123",
            agent_id="agent-456",
            tool_name="tool_a",
            arguments_sha256="abc",
            decision="ALLOWED",
            created_at_iso="2024-01-01T00:00:00+00:00",
        )
        hash2 = compute_event_hash(
            prev_hash="0" * 64,
            sequence_num=1,
            org_id="org-123",
            agent_id="agent-456",
            tool_name="tool_b",
            arguments_sha256="abc",
            decision="ALLOWED",
            created_at_iso="2024-01-01T00:00:00+00:00",
        )
        assert hash1 != hash2