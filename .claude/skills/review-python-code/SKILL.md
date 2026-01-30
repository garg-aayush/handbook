---
name: review-python-code
description: Review Python code for ML, APIs, and deployment. Use when reviewing Python files for machine learning, API requests, or deployment code.
---

Review Python code for bugs, edge cases, and pitfalls in ML/API/deployment contexts.

## Rules
- **Input Required**: If no files provided, ask user to reference specific files.
- **Correctness > Style**: Skip PEP8 nitpicks. Focus on bugs and logic errors.
- **No Edits**: Report issues in chat only—do not modify files.

## Focus Areas
**ML & Data**
- Data leakage (train/test contamination), incorrect tensor shapes, wrong device (CPU/GPU)
- Model state issues (missing `eval()`, gradient accumulation), incorrect loss/metric usage
- NumPy/Pandas pitfalls: chained indexing, dtype mismatches, broadcasting errors

**APIs & Requests**
- Missing error handling, timeouts, retries for network calls
- Auth token exposure, missing validation on inputs/responses
- Rate limiting, connection pooling, async misuse

**Deployment**
- Hardcoded secrets/paths, missing env var checks
- Resource leaks (unclosed files/connections), memory issues
- Missing dependency version pins, incompatible package versions

## Output Format
1. **Critical**: Bugs causing crashes or wrong results
2. **Edge Cases**: Unhandled scenarios
3. **Fixes**: Brief code snippets for corrections
