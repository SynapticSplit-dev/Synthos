# Intelligence workflow

The intelligence layer interprets user intent using keyword-based classification. This is intentionally lightweight and transparent.

## Implemented intent classes

- memory_retrieval
- training
- inference
- monitoring
- general_reasoning

## Interface

The `IntelligenceEngine.interpret()` method returns a structured result with intent, confidence, context and answer.
