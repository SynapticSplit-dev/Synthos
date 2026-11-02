# Development guide

The project is designed for local development and controlled extension.

## Typical workflow

1. update a module in `backend/app/synthos`
2. add a focused test in `backend/tests`
3. run `pytest`
4. update docs if architecture changes

## Responsibility boundaries

- keep modules explicit
- preserve backward-compatible interfaces where possible
- avoid over-engineering
