from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SystemConfig:
    app_name: str = "SYNTHOS"
    version: str = "0.1.0"
    log_level: str = "INFO"
    max_memory_entries: int = 256
    default_model_dim: int = 32
    default_hidden_dim: int = 64
    training_epochs: int = 3


@dataclass
class WorkflowResult:
    workflow_name: str
    success: bool
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class SynthosCore:
    """Core registry and lifecycle manager for the SYNTHOS runtime."""

    def __init__(self, config: SystemConfig | None = None):
        self.config = config or SystemConfig()
        self.registry: dict[str, Any] = {}
        self._status: dict[str, Any] = {
            "app": self.config.app_name,
            "version": self.config.version,
            "ready": True,
            "modules": [],
        }

    def register_module(self, name: str, module: Any) -> None:
        self.registry[name] = module
        self._status["modules"] = sorted(self.registry)

    def status(self) -> dict[str, Any]:
        return {
            "app": self.config.app_name,
            "version": self.config.version,
            "ready": self._status["ready"],
            "modules": self._status["modules"],
        }
