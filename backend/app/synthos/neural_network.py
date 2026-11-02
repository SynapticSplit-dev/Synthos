from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np


@dataclass
class NeuralConfig:
    vocab_size: int = 128
    embedding_dim: int = 16
    hidden_dim: int = 32
    lr: float = 0.01
    seed: int = 42


class TinyNeuralNetwork:
    """Small feed-forward network used for deterministic vector encoding and classification."""

    def __init__(self, config: NeuralConfig | None = None):
        self.config = config or NeuralConfig()
        self.rng = np.random.default_rng(self.config.seed)
        self.embedding = self.rng.normal(0.0, 0.5, size=(self.config.vocab_size, self.config.embedding_dim))
        self.w1 = self.rng.normal(0.0, 0.5, size=(self.config.embedding_dim, self.config.hidden_dim))
        self.b1 = np.zeros(self.config.hidden_dim)
        self.w2 = self.rng.normal(0.0, 0.5, size=(self.config.hidden_dim, 2))
        self.b2 = np.zeros(2)

    def _token_to_vector(self, token: str) -> np.ndarray:
        index = abs(hash(token)) % self.config.vocab_size
        return self.embedding[index]

    def encode(self, tokens: list[str]) -> np.ndarray:
        if not tokens:
            return np.zeros(self.config.embedding_dim)
        vectors = np.stack([self._token_to_vector(token) for token in tokens])
        return vectors.mean(axis=0)

    def forward(self, feature_vector: np.ndarray) -> np.ndarray:
        hidden = feature_vector @ self.w1 + self.b1
        hidden = np.tanh(hidden)
        output = hidden @ self.w2 + self.b2
        return output

    def compute_loss(self, logits: np.ndarray, target: int) -> float:
        logits = logits - np.max(logits)
        probs = np.exp(logits)
        probs = probs / probs.sum()
        return -math.log(probs[target] + 1e-12)

    def train_step(self, tokenized_input: list[str], target: int) -> dict[str, float]:
        feature = self.encode(tokenized_input)
        hidden = np.tanh(feature @ self.w1 + self.b1)
        logits = hidden @ self.w2 + self.b2
        loss = self.compute_loss(logits, target)
        grad_out = np.zeros_like(logits)
        probs = np.exp(logits - np.max(logits))
        probs = probs / probs.sum()
        grad_out[target] = probs[target] - 1.0
        grad_w2 = np.outer(hidden, grad_out)
        grad_b2 = grad_out
        grad_hidden = grad_out @ self.w2.T * (1.0 - hidden ** 2)
        grad_w1 = np.outer(feature, grad_hidden)
        grad_b1 = grad_hidden

        self.w2 -= self.config.lr * grad_w2
        self.b2 -= self.config.lr * grad_b2
        self.w1 -= self.config.lr * grad_w1
        self.b1 -= self.config.lr * grad_b1
        return {"loss": float(loss), "prediction": int(np.argmax(logits))}

    def save_checkpoint(self, path: str | Path) -> str:
        payload = {
            "config": {
                "vocab_size": self.config.vocab_size,
                "embedding_dim": self.config.embedding_dim,
                "hidden_dim": self.config.hidden_dim,
                "lr": self.config.lr,
                "seed": self.config.seed,
            },
            "embedding": self.embedding.tolist(),
            "w1": self.w1.tolist(),
            "b1": self.b1.tolist(),
            "w2": self.w2.tolist(),
            "b2": self.b2.tolist(),
        }
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload), encoding="utf-8")
        return str(destination)

    def load_checkpoint(self, path: str | Path) -> "TinyNeuralNetwork":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        self.config = NeuralConfig(**payload["config"])
        self.embedding = np.array(payload["embedding"], dtype=float)
        self.w1 = np.array(payload["w1"], dtype=float)
        self.b1 = np.array(payload["b1"], dtype=float)
        self.w2 = np.array(payload["w2"], dtype=float)
        self.b2 = np.array(payload["b2"], dtype=float)
        return self
