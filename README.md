# SYNTHOS

SYNTHOS is a modular AI runtime focused on input processing, reasoning, memory, learning, inference, and workflow orchestration. This repository now contains a coherent local implementation using Python and lightweight machine learning primitives, while preserving the existing backend foundation.

## Project vision

The goal of SYNTHOS is to provide a clear, extensible architecture for an AI system that can execute locally and remain understandable. The codebase deliberately favors small but working components over unsupported large-scale claims.

## Core architecture

- Core runtime: central module registry and lifecycle manager
- Input processing: text normalization, tokenization, and payload preparation
- Intelligence engine: intent classification and reasoning
- Memory system: in-memory working, short-term, semantic, and retrieval context
- Neural network: small feed-forward model for encoding and prediction
- Training workflow: lightweight local optimization loop
- Inference workflow: prediction over user text
- Orchestration: end-to-end execution across runtime components

## Current capabilities

- raw text normalization and tokenization
- rule-based intent understanding
- memory add/search/update/expire operations
- compact neural network with forward pass and checkpoint persistence
- training and inference workflow APIs
- automated workflow tests
- architecture documentation and Mermaid diagrams

## Technology stack

- Python 3.11+
- NumPy
- FastAPI
- SQLAlchemy
- Pydantic and Pydantic settings
- pytest
- Markdown and Mermaid documentation

## Repository structure

```text
SYNTHOS/
├── README.md
├── .env.example
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── synthos/
│   ├── tests/
│   └── pyproject.toml
├── docs/
│   ├── README.md
│   ├── PROJECT_VISION.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── TECH_STACK.md
│   ├── REPOSITORY_STRUCTURE.md
│   ├── architecture/
│   ├── workflows/
│   ├── neural-networks/
│   ├── memory/
│   ├── development/
│   ├── roadmap/
│   └── diagrams/
├── docker-compose.yml
├── LICENSE
└── Makefile
```

## Installation

```bash
cd /path/to/Synthos
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy pytest fastapi sqlalchemy pydantic pydantic-settings httpx redis asyncpg argon2-cffi pyjwt structlog
```

## Configuration

Use the example environment file and adjust the values for your local execution context:

```bash
cp .env.example .env
```

## Running the app

```bash
cd backend
PYTHONPATH=. python -m app.main
```

## Testing

```bash
cd backend
PYTHONPATH=. pytest -q
```

## Training and inference

```python
from app.synthos.training import TrainingWorkflow
from app.synthos.inference import InferenceWorkflow

training = TrainingWorkflow()
history = training.fit([["learn", "model"], ["system", "memory"]], [0, 1], epochs=2)
print(history)

inference = InferenceWorkflow()
print(inference.run("remember the training result"))
```

## Current implementation status

This repository currently includes:

- functional runtime registry and orchestration
- input processing and tokenization
- in-memory memory management
- compact neural network implementation
- inference and training workflows
- documentation tree and architecture diagrams
- automated tests covering core workflow behavior

## Known limitations

- memory is currently in-memory rather than persistent
- model is intentionally lightweight rather than large-scale
- functionality is local-development oriented and transparent
- extended transformer architecture is planned rather than implemented

## Final note

This project is intended to be a working and technically understandable implementation of the SYNTHOS architecture without claiming capabilities beyond the code that has actually been built and tested.
