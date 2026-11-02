# Overall architecture

## Static overview

```mermaid
flowchart LR
    A[User Input] --> B[InputProcessor]
    B --> C[IntelligenceEngine]
    B --> D[MemoryStore]
    C --> E[TinyNeuralNetwork]
    D --> F[SynthosOrchestrator]
    E --> G[Inference / Training Outputs]
    F --> H[Memory Update]
    H --> D
```

## Design notes

This diagram captures the current working architecture: input enters the system, is normalized, processed by intelligence and memory, then passed to the model, which returns a result that updates memory and workflow state.
