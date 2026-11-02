# SYNTHOS

SYNTHOS is a compact AI system architecture built around a modular runtime, neural network primitives, memory subsystems, and workflow orchestration. The project centers on a simple but extensible Python implementation that can be developed and tested locally without requiring enterprise-scale infrastructure.

## Vision

The project aims to provide a coherent and understandable architecture for:

- input processing and normalization
- reasoning and task interpretation
- neural feature encoding and inference
- in-memory memory management
- workflow coordination
- training and evaluation loops
- documentation and maintenance

## Objectives

- Build a clear, maintainable AI system structure.
- Keep the runtime modular and testable.
- Use a small neural network that works in constrained environments.
- Provide memory operations for working, semantic, and short-term contexts.
- Document the architecture and lifecycle clearly.
- Deliver a working end-to-end workflow with actual code and tests.

## Core Architecture

SYNTHOS combines a runtime registry, input processor, memory store, neural network, intelligence engine, and orchestrator. These components are wired together in a central runtime builder and exposed through a small set of Python interfaces.

## Main Capabilities

- Text normalization and tokenization
- intent classification
- memory add/search/update/expire flows
- inference over tokenized inputs
- checkpoint save/load for the neural model
- training workflow with loss and accuracy metrics
- documentation and diagrammatic architecture reference

## Neural Network Architecture

The current implementation uses a compact feed-forward neural network with:

- embedding lookup derived from token hash
- feature vector projection into a hidden layer
- tanh activation
- classification output layer
- deterministic training step and loss computation

This is intentionally lightweight and appropriate for a local repository implementation rather than a large production language model.

## Memory Architecture

The memory layer supports:

- working memory
- short-term memory
- semantic memory
- retrieval by content overlap
- context reconstruction
- expiration logic

## Workflow Overview

The project includes workflow stages for:

1. input processing
2. reasoning and task interpretation
3. memory management
4. neural processing
5. inference and prediction
6. training and evaluation

## Technology Stack

- Python 3.11+
- NumPy
- FastAPI (existing backend foundation)
- SQLAlchemy / PostgreSQL-ready configuration
- Pydantic settings
- pytest

## Repository Structure

- backend/app/synthos: SYNTHOS runtime modules
- backend/app/core: existing security and ledger utilities
- backend/app/models: SQLAlchemy models
- backend/tests: automated tests
- docs: architecture and project documentation

## Installation

```bash
cd /path/to/Synthos
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy pytest fastapi sqlalchemy pydantic pydantic-settings httpx redis asyncpg argon2-cffi pyjwt structlog
```

## Environment Configuration

Copy the example environment file and adjust the values:

```bash
cp .env.example .env
```

## Running the Project

```bash
cd backend
PYTHONPATH=. python -m app.main
```

## Testing

```bash
cd backend
PYTHONPATH=. pytest -q
```

## Training

```python
from app.synthos.training import TrainingWorkflow

workflow = TrainingWorkflow()
examples = [["hello", "world"], ["memory", "retrieval"], ["train", "model"]]
labels = [0, 1, 1]
print(workflow.fit(examples, labels, epochs=5))
```

## Inference

```python
from app.synthos.inference import InferenceWorkflow

workflow = InferenceWorkflow()
print(workflow.run("remember the previous result"))
```

## Development Roadmap

- complete architecture and documentation
- expand model capability and memory indexing
- improve workflow interfaces and validation
- add richer inference and training pipelines
- support persistent storage and retrieval

## Current Status

The project currently includes:

- runtime registry and orchestration
- input processing and tokenization
- memory store with search and expiry
- neural network implementation
- inference and training workflows
- test suite and architecture documentation

## Known Limitations

- the neural model is intentionally lightweight
- memory is in-memory rather than durable storage-backed
- the system is designed for local execution and experimentation
- production-scale language modeling is not implied by the current implementation

---

This repository provides a working local foundation for SYNTHOS and a faithful implementation trail that matches the specification without inventing unsupported large-scale capabilities.
