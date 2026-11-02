# Input processing workflow

The input workflow validates raw text, normalizes whitespace, strips empty content, and tokenizes accepted text.

## Input contract

- string input
- optional metadata dictionary

## Output contract

```python
InputRecord(
    raw_text='...',
    normalized_text='...',
    tokens=['...'],
    metadata={...}
)
```

## Implementation

The InputProcessor lives in `backend/app/synthos/input_processing.py`.
