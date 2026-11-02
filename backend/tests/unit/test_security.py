import pytest
import string

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    generate_agent_api_key,
    verify_agent_api_key,
)


class TestPasswordHashing:
    def test_hash_password_returns_string(self):
        hashed = hash_password("testpassword123")
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != "testpassword123"

    def test_verify_password_correct(self):
        hashed = hash_password("testpassword123")
        assert verify_password("testpassword123", hashed) is True

    def test_verify_password_incorrect(self):
        hashed = hash_password("testpassword123")
        assert verify_password("wrongpassword", hashed) is False

    def test_verify_password_malformed_hash(self):
        assert verify_password("testpassword123", "not-a-valid-hash") is False


class TestJWT:
    def test_create_and_decode_access_token(self):
        token = create_access_token(
            user_id="user-123",
            org_id="org-456",
            role="ADMIN",
            expires_minutes=60,
        )
        assert isinstance(token, str)
        assert len(token) > 0

        decoded = decode_access_token(token)
        assert decoded["sub"] == "user-123"
        assert decoded["org_id"] == "org-456"
        assert decoded["role"] == "ADMIN"
        assert "iat" in decoded
        assert "exp" in decoded

    def test_decode_invalid_token(self):
        with pytest.raises(Exception):
            decode_access_token("invalid.token.string")


class TestAgentAPIKey:
    def test_generate_agent_api_key_format(self):
        pepper = "test_pepper_12345"
        raw_key, prefix, key_hash = generate_agent_api_key(pepper)

        assert raw_key.startswith("tl_live_")
        parts = raw_key.split("_")
        # tl_live_<12_char_alnum>_<32_char_hex> -> 4 parts when split by _
        assert len(parts) == 4
        assert parts[0] == "tl"
        assert parts[1] == "live"
        assert len(parts[2]) == 12  # prefix
        assert all(c in string.ascii_lowercase + string.digits for c in parts[2])
        assert len(parts[3]) == 32  # hex secret
        assert all(c in "0123456789abcdef" for c in parts[3])
        assert prefix.startswith("tl_live_")
        assert len(key_hash) == 64  # SHA-256 hex digest

    def test_verify_agent_api_key_correct(self):
        pepper = "test_pepper_12345"
        raw_key, prefix, key_hash = generate_agent_api_key(pepper)
        assert verify_agent_api_key(raw_key, key_hash, pepper) is True

    def test_verify_agent_api_key_wrong(self):
        pepper = "test_pepper_12345"
        raw_key, prefix, key_hash = generate_agent_api_key(pepper)
        # Tamper with the key
        tampered_key = raw_key[:-5] + "XXXXX"
        assert verify_agent_api_key(tampered_key, key_hash, pepper) is False

    def test_verify_agent_api_key_wrong_hash(self):
        pepper = "test_pepper_12345"
        raw_key, prefix, key_hash = generate_agent_api_key(pepper)
        assert verify_agent_api_key(raw_key, "0" * 64, pepper) is False

    def test_generate_unique_keys(self):
        pepper = "test_pepper_12345"
        _, _, hash1 = generate_agent_api_key(pepper)
        _, _, hash2 = generate_agent_api_key(pepper)
        assert hash1 != hash2