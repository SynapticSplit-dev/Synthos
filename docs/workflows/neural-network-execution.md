# Neural network execution workflow

The neural network workflow uses a compact feed-forward model for feature encoding and classification.

## Internal flow

```mermaid
flowchart LR
    A[Tokens] --> B[Embedding Lookup]
    B --> C[Feature Averaging]
    C --> D[Hidden Layer]
    D --> E[Output Layer]
    E --> F[Prediction]
```

## Current implementation

The `TinyNeuralNetwork` in `backend/app/synthos/neural_network.py` provides forward pass, loss calculation, and training step logic.
