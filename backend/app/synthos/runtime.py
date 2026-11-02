from __future__ import annotations

from pathlib import Path

from app.synthos.core import SynthosCore, SystemConfig
from app.synthos.input_processing import InputProcessor
from app.synthos.intelligence import IntelligenceEngine
from app.synthos.memory import MemoryStore
from app.synthos.neural_network import TinyNeuralNetwork
from app.synthos.orchestrator import SynthosOrchestrator


def build_runtime() -> SynthosCore:
    config = SystemConfig(app_name="SYNTHOS", version="0.1.0", log_level="INFO")
    core = SynthosCore(config=config)
    core.register_module("input_processing", InputProcessor())
    core.register_module("memory", MemoryStore(max_entries=128))
    core.register_module("intelligence", IntelligenceEngine())
    core.register_module("neural_network", TinyNeuralNetwork())
    core.register_module("orchestrator", SynthosOrchestrator())
    return core


__all__ = ["build_runtime", "SynthosCore", "SystemConfig"]
