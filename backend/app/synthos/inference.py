from __future__ import annotations

import numpy as np

from app.synthos.input_processing import InputProcessor
from app.synthos.neural_network import TinyNeuralNetwork


class InferenceWorkflow:
    """Run model inference over user text."""

    def __init__(self, model: TinyNeuralNetwork | None = None):
        self.model = model or TinyNeuralNetwork()
        self.input_processor = InputProcessor()

    def predict(self, text: str) -> dict[str, object]:
        tokens = self.input_processor.tokenize(text)
        feature = self.model.encode(tokens or ["synthos"])
        logits = self.model.forward(feature)
        probabilities = np.exp(logits - np.max(logits))
        probabilities = probabilities / probabilities.sum()
        predicted_index = int(np.argmax(logits))
        return {
            "tokens": tokens,
            "prediction": predicted_index,
            "logits": logits.tolist(),
            "probabilities": probabilities.tolist(),
            "label": f"class_{predicted_index}",
        }

    def run(self, text: str) -> dict[str, object]:
        return self.predict(text)


__all__ = ["InferenceWorkflow"]
