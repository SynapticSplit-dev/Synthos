from __future__ import annotations

import pytest

from app.synthos.core import SynthosCore, SystemConfig
from app.synthos.inference import InferenceWorkflow
from app.synthos.input_processing import InputProcessor
from app.synthos.memory import MemoryStore
from app.synthos.neural_network import NeuralConfig, TinyNeuralNetwork
from app.synthos.orchestrator import SynthosOrchestrator
from app.synthos.training import TrainingWorkflow


def test_runtime_initializes():
    core = SynthosCore(config=SystemConfig(app_name="SYNTHOS", version="0.2.0"))
    assert core.config.app_name == "SYNTHOS"
    assert core.status()["ready"] is True

    core.register_module("demo", {"id": 1})
    assert "demo" in core.registry


def test_input_processing_normalizes_text():
    processor = InputProcessor()
    record = processor.prepare("  Hello   world  ")
    assert record.normalized_text == "Hello world"
    assert record.tokens == ["hello", "world"]


def test_memory_store_round_trip_and_search():
    memory = MemoryStore(max_entries=8)
    memory.add("m1", "remember the training result", "semantic")
    memory.add("m2", "the system is running", "working")

    assert len(memory.get(memory_type="semantic")) == 1
    assert memory.search("training")[0].key == "m1"

    updated = memory.update("m1", "remember the updated result", "semantic")
    assert updated is not None and updated.content == "remember the updated result"


def test_memory_expiration_and_reconstruction():
    memory = MemoryStore(max_entries=8)
    memory.add("expiring", "temporary note", "working", ttl=0.01)
    expired = memory.expire()
    assert isinstance(expired, list)
    assert memory.reconstruct_context() == ""


def test_neural_network_forward_pass_dimensions():
    model = TinyNeuralNetwork(NeuralConfig(vocab_size=50, embedding_dim=8, hidden_dim=16))
    feature = model.encode(["alpha", "beta"])
    logits = model.forward(feature)
    assert feature.shape == (8,)
    assert logits.shape == (2,)


def test_training_step_and_loss_are_numeric():
    model = TinyNeuralNetwork()
    result = model.train_step(["sample", "training", "text"], target=1)
    assert "loss" in result
    assert isinstance(result["loss"], float)
    assert result["prediction"] in (0, 1)


def test_checkpoint_round_trip():
    model = TinyNeuralNetwork(NeuralConfig(vocab_size=32, embedding_dim=8, hidden_dim=12))
    path = "/tmp/synthos_checkpoint.json"
    saved = model.save_checkpoint(path)
    loaded = model.load_checkpoint(saved)
    assert loaded is model
    assert model.embedding.shape == (32, 8)


def test_training_workflow_runs_epoch():
    workflow = TrainingWorkflow(model=TinyNeuralNetwork(NeuralConfig(vocab_size=64, embedding_dim=8, hidden_dim=12)))
    examples = [["learn", "model"], ["memory", "response"], ["system", "status"]]
    labels = [0, 1, 1]
    history = workflow.fit(examples, labels, epochs=2)
    assert len(history) == 2
    assert history[-1]["accuracy"] >= 0.0


def test_inference_workflow_outputs_prediction():
    workflow = InferenceWorkflow(model=TinyNeuralNetwork(NeuralConfig(vocab_size=64, embedding_dim=8, hidden_dim=12)))
    payload = workflow.run("remember the training result")
    assert payload["prediction"] in (0, 1)
    assert len(payload["logits"]) == 2
    assert len(payload["probabilities"]) == 2


def test_orchestrator_executes_workflow():
    orchestrator = SynthosOrchestrator()
    payload = orchestrator.run_workflow("Train the memory model and answer the query")
    assert payload["success"] is True
    assert payload["intent"] in {"training", "memory_retrieval", "general_reasoning", "inference", "monitoring"}
    assert "tokens" in payload


def test_input_validation_error_is_raised_for_non_string():
    processor = InputProcessor()
    with pytest.raises(TypeError):
        processor.normalize(123)  # type: ignore[arg-type]


def test_training_rejects_mismatched_examples_and_labels():
    workflow = TrainingWorkflow()
    with pytest.raises(ValueError):
        workflow.fit([["x"]], [0, 1])
