from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.synthos.core import WorkflowResult
from app.synthos.input_processing import InputProcessor
from app.synthos.intelligence import IntelligenceEngine
from app.synthos.memory import MemoryStore
from app.synthos.neural_network import TinyNeuralNetwork


@dataclass
class WorkflowContext:
    source_text: str
    normalized_text: str
    tokens: list[str]
    memory: MemoryStore
    model: TinyNeuralNetwork
    reasoning: IntelligenceEngine
    metrics: dict[str, Any] = field(default_factory=dict)


class SynthosOrchestrator:
    """Coordinates the major workflow stages for SYNTHOS."""

    def __init__(self):
        self.input_processor = InputProcessor()
        self.memory = MemoryStore(max_entries=128)
        self.model = TinyNeuralNetwork()
        self.reasoning = IntelligenceEngine()

    def run_workflow(self, text: str) -> dict[str, Any]:
        record = self.input_processor.prepare(text)
        self.memory.add(key="input", content=record.normalized_text, memory_type="working")

        reasoning = self.reasoning.interpret(record.normalized_text)
        feature = self.model.encode(record.tokens or ["synthos"])
        logits = self.model.forward(feature)
        category = int(__import__("numpy").argmax(logits))

        self.memory.add(key="reasoning", content=reasoning.answer, memory_type="semantic")
        self.memory.add(key="response", content=f"Processed: {record.normalized_text}", memory_type="short_term")

        result = {
            "workflow": "SYNTHOS_MAIN",
            "success": True,
            "text": record.normalized_text,
            "tokens": record.tokens,
            "intent": reasoning.intent,
            "confidence": reasoning.confidence,
            "prediction_class": category,
            "memory_summary": self.memory.stats(),
            "context": self.memory.reconstruct_context(5),
        }
        return result

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "module_count": 3,
            "memory": self.memory.stats(),
        }
