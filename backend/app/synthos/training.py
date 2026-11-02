from __future__ import annotations

from app.synthos.neural_network import TinyNeuralNetwork


class TrainingWorkflow:
    """Run lightweight training and return epoch summaries."""

    def __init__(self, model: TinyNeuralNetwork | None = None):
        self.model = model or TinyNeuralNetwork()

    def fit(self, examples: list[list[str]], labels: list[int], epochs: int = 1) -> list[dict[str, float]]:
        if len(examples) != len(labels):
            raise ValueError("Examples and labels must match in length.")
        if not examples:
            raise ValueError("At least one training example is required.")

        history: list[dict[str, float]] = []
        for epoch in range(1, epochs + 1):
            losses: list[float] = []
            correct = 0
            for tokens, target in zip(examples, labels):
                info = self.model.train_step(tokens, int(target))
                losses.append(float(info["loss"]))
                if int(info["prediction"]) == int(target):
                    correct += 1
            history.append(
                {
                    "epoch": float(epoch),
                    "loss": sum(losses) / len(losses),
                    "accuracy": correct / len(labels),
                }
            )
        return history

    def train_epoch(self, examples: list[list[str]], labels: list[int]) -> dict[str, float]:
        return self.fit(examples, labels, epochs=1)[0]


__all__ = ["TrainingWorkflow"]
