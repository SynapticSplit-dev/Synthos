# Troubleshooting

Common issues include:

- missing Python dependencies
- missing environment variables
- bad PYTHONPATH settings
- invalid or stale `.env` values

If a test fails, run with verbose output:

```bash
PYTHONPATH=. pytest -vv
```
